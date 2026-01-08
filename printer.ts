const { crc32 } = window.require('crc');

    private SendToPrinter(data: string): void {

        data = data + '\n';

        if (this.PrinterDebugMonitor) {
            this.PrinterDebugMonitor.LogDataToPrinter(data);
        }

        this.printerConnection.write(data);
    }

    /**
     * Send some data to the printer.
     * @param data The data to send.
     */
    private SendBufferToPrinter(data: Buffer): void {

        if (this.PrinterDebugMonitor != null) {
            this.PrinterDebugMonitor.LogDataToPrinter(data.toString());
        }

        this.printerConnection.write(data);
    }


    /**
     * Instructs the printer to print a file already stored in its internal storage.
     * @param fileName The file name (including extension) of the file to print.
     */
    PrintFileAsync(fileName: string): Promise<void> {
        this.ValidatePrinterReady();
        const message = '~' + MachineCommands.PrintFileFromSd + ' 0:/user/' + fileName;
        this.SendToPrinter(message);

        return this.WaitForPrinterAck(MachineCommands.PrintFileFromSd);
    }

        /**
     * Transfers a file to the printer's storage with a given name.
     * @param filePath The path to the file to transfer.
     * @param fileName The name of the file to store it as (without file extension)
     */
    StoreFileAsync(filePath: string, fileName: string): PromiseWithProgress<void> {
        return new PromiseWithProgress<void>((updateProgress: (value: number) => void) => {
            return this.StoreFileAsyncInternal(filePath, fileName, updateProgress);
        });
    }

    /**
     * Transfers a file to the printer's storage with a given name.
     * @param filePath The path to the file to transfer.
     * @param fileName The name of the file to store it as (without file extension)
     * @param updateProgress The function to cal with progress updates
     */
    private async StoreFileAsyncInternal(filePath: string, fileName: string, updateProgress: (number: number) => void): Promise<void> {
        this.ValidatePrinterReady();

        // Load the file from disk
        const modelBytes = await new Promise<Buffer>((a, r) => {
            fs.readFile(filePath, (error: any, data: any) => {
                if (error) {
                    r(error);
                }

                a(data);
            });
        });

        // Start a transfer
        ErrorLogger.Trace("Starting file transfer");
        let message = '~' + MachineCommands.BeginWriteToSdCard + ' ' + modelBytes.length + ' 0:/user/' + fileName;
        this.SendToPrinter(message);
        await this.WaitForPrinterAck(MachineCommands.BeginWriteToSdCard);

        let count = 0;
        let offset = 0;
        while (offset < modelBytes.length) {
            let crc: number;
            let packet: Buffer;

            let dataSize = 0;
            if (offset + this.packetSizeBytes < modelBytes.length) {
                packet = modelBytes.subarray(offset, offset + this.packetSizeBytes);

                const crcResult = crc32(packet);
                crc = crcResult;
                dataSize = this.packetSizeBytes;
            }
            else {
                // Every packet needs to be the same size, so zero pad the last one if we need to.
                const actualLength = modelBytes.length - offset;
                const data = modelBytes.subarray(offset, actualLength + offset);

                // The CRC is for the un-padded data.
                const crcResult = crc32(data);
                crc = crcResult;

                packet = Buffer.alloc(this.packetSizeBytes);
                for (let i = 0; i < data.length; ++i) {
                    packet.writeUInt32LE(data[i], i);
                }

                packet.fill(null, actualLength, this.packetSizeBytes);

                dataSize = actualLength;
            }

            // Always start each packet with four bytes
            const bufferToSend = Buffer.alloc(this.packetSizeBytes + 16);
            bufferToSend.writeUInt16LE(0x5a, 0);
            bufferToSend.writeUInt16LE(0x5a, 1);
            bufferToSend.writeUInt16LE(0xef, 2);
            bufferToSend.writeUInt16LE(0xbf, 3);

            // Add the count of this packet, the size of the data it in (not counting padding) and the CRC.
            bufferToSend.writeUInt32BE(count, 4);
            bufferToSend.writeUInt32BE(dataSize, 8);
            bufferToSend.writeUInt32BE(crc, 12);

            // Add the data
            for (let i = 0; i < packet.length; ++i) {
                bufferToSend.writeUInt8(packet[i], i + 16);
            }

            // Send it to the printer
            this.SendBufferToPrinter(bufferToSend);

            // Update the progress
            const progress = offset / modelBytes.length;
            updateProgress(progress);

            offset += this.packetSizeBytes;
            ++count;
        }

        this.SendToPrinter('');

        // Tell the printer that we have finished the file transfer
        ErrorLogger.Trace("Ending file transfer");
        message = '~' + MachineCommands.EndWriteToSdCard;

        this.SendToPrinter(message);

        return this.WaitForPrinterAck(MachineCommands.EndWriteToSdCard);
    }

    /**
     * Waits fot the printer to acknowledge that a command send to it completed.
     */
    private async WaitForPrinterAck(commandId: string): Promise<void> {
        await this.responseReader.GerPrinterResponse<IPrinterResponse>(commandId);
    }



