# An api to send and receive GCode commands and files to the Adventurer 3 3D Printer via TCP.
# https://github.com/georgewoodall82/Adv3GUI/blob/main/Adv3Api.py
import socket
import messageWindow as msg
import tqdm
import struct
import binascii #https://lindevs.com/calculate-crc32-checksum-using-python/


packetSizeBytes = 4096
socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET is a socket address family constant for the Internet address family.
# socket.SOCK_STREAM is a socket type constant for TCP/IP stream sockets.


def Connect(ip: str, port=8899):
    # Connect to the printer at the given ip and port.
    # Returns a socket object.
    try:
        socket1.connect((ip, port))
    except:
        return False
    return True


def SendGCode(gcode):
    # Send the given gcode to the printer.
    # Returns the response from the printer.

    gcode = "~" + gcode + "\n"

    return SendTCP(gcode)

# Send the given data to the printer in bytes.


def SendBytes(data):
    print("SOCKET: Sending raw data...")
    socket1.send(data)


def SendTCP(data):
    # Send the given data to the printer.
    # Returns the response from the printer.
    print("SOCKET: Sending: " + data)
    socket1.send(data.encode())
    out = socket1.recv(4096).decode()
    print("SOCKET: Received: \"" + out + "\"")
    return out

def SendTCPWithoutReading(data):
    # Send the given data to the printer.
    # Returns the response from the printer.
    print("SOCKET: Sending: " + data)
    socket1.send(data.encode())


def Disconnect():
    # Disconnect from the printer but keep the socket open.
    # Returns nothing.
    if isConnected():
        socket1.close()


def isConnected():
    # Check if the printer is connected.
    # Returns True if connected, False otherwise.
    try:
        socket1.send("~".encode())
        return True
    except:
        return False

class MachineCommands:
    GetEndstopStatus = 'M119'
    BeginWriteToSdCard = 'M28'
    EndWriteToSdCard = 'M29'
    PrintFileFromSd = 'M23'
    GetFirmwareVersion = 'M115'
    GetTemperature = 'M105'
    StopPrinting = 'M26'
    PausePrinting = 'M25'
    ResumePrinting = 'M24'
    LedOn = 'M146 r255 g255 b255 F0'
    LedOff = 'M146 r0 g0 b0 F0'
    printingStatus = 'M27'
    getPosition = 'M114'
    emergencyStop = 'M112'
    activateBackFan = 'M651'
    deactivateBackFan = 'M652'
#More commands here: https://take4-blue.com/en/3d-printer/adventurer3-control-3/
#and here https://github.com/take4blue/PrintControler/blob/master/PrintControler/Adventurer3Controler.cs

def StopPrinting():
    # Stops the printing.
    return SendGCode(MachineCommands.StopPrinting)


def PausePrinting():
    # Pauses the printing.
    return SendGCode(MachineCommands.PausePrinting)


def ResumePrinting():
    # Resumes the printing.
    return SendGCode(MachineCommands.ResumePrinting)


def GetPrinterStatus():
    # Get the printer status.
    return SendGCode(MachineCommands.GetEndstopStatus)


def GetFirmwareVersion():
    # Get the firmware version.
    return SendGCode(MachineCommands.GetFirmwareVersion)


def GetTemperature():
    # Get the temperature.
    return SendGCode(MachineCommands.GetTemperature)

def SetNozzleTemperature(temperature):
#     M140 S80 T0
# M104 S230 T0
    return SendGCode('M104 S' + str(temperature)+' T0')

def SetBedTemperature(temperature):
    return SendGCode('M140 S' + str(temperature)+' T0')

def EnableLED():
    return SendGCode(MachineCommands.LedOn)

def DisableLED():
    return SendGCode(MachineCommands.LedOff)

def ActivateBackFan():
    return SendGCode(MachineCommands.activateBackFan)

def DeactivateBackFan():
    return SendGCode(MachineCommands.deactivateBackFan)

def GetPosition():
    return SendGCode(MachineCommands.getPosition)

def PrintFile(filename): # Instructs the printer to print a file already stored in its internal storage.
    return SendGCode(MachineCommands.PrintFileFromSd + ' 0:/user/' + filename)


"""
Basic flow of commands when printing
* Data is transferred at M28 to M29, and printing is started at M23.
If you want to stop the molding, send M26. If it is M112, a nozzle etc. will not stop at the place now (unverified).
Since communication with the device has to be repeated within 10 seconds, the condition of the device is monitored by M119, M105 and M27 even after the M28 is sent.
"""

def StoreFile(pcFilePath, printerFileName):
    print("Uploading file in path:", pcFilePath, "as", printerFileName)
    in_file = open(pcFilePath, "rb")  # opening for [r]eading as [b]inary
    modelBytes = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()
    print("File read. Bytes:", len(modelBytes))

    SendGCode(MachineCommands.BeginWriteToSdCard + ' ' +
              str(len(modelBytes)) + ' 0:/user/' + printerFileName)

    count = 0
    offset = 0
    # pbar = tqdm.tqdm(total=len(modelBytes))
# pbar.update(packetSizeBytes)

    while offset < len(modelBytes):
        crc = 0
        packet = b''

        dataSize = 0
        if offset + packetSizeBytes < len(modelBytes):
            print("\tSending full packet.")
            packet = modelBytes[offset:offset + packetSizeBytes]
            crc = crc32(packet)
            dataSize = packetSizeBytes
        else:
            print("\tSending last packet.")
            # Every packet needs to be the same size, so zero pad the last one if we need to.
            actualLength = len(modelBytes) - offset
            data = modelBytes[offset:actualLength + offset]
            crc = crc32(data)

            # packet = Buffer.alloc(this.packetSizeBytes);
            #     for (let i = 0; i < data.length; ++i) {
            #         packet.writeUInt32LE(data[i], i);
            #     }
            packet = b''
            for i in range(len(data)):
                packet += struct.pack('<I', data[i])

            #packet.fill(null, actualLength, this.packetSizeBytes);
            packet += b'\x00' * (packetSizeBytes - actualLength)
            dataSize = actualLength

        # Always start each packet with four bytes
        bufferToSend = b''

        # bufferToSend.writeUInt16LE(0x5a, 0);
        # bufferToSend.writeUInt16LE(0x5a, 1);
        # bufferToSend.writeUInt16LE(0xef, 2);
        # bufferToSend.writeUInt16LE(0xbf, 3);

        # // Add the count of this packet, the size of the data it in (not counting padding) and the CRC.
        # bufferToSend.writeUInt32BE(count, 4);
        # bufferToSend.writeUInt32BE(dataSize, 8);
        # bufferToSend.writeUInt32BE(crc, 12);


        print("\tHEADER: Packet count:",count,"Data size:",dataSize,", Crc:",crc)
        bufferToSend += struct.pack('<I', 0x5a5a5a5a)
        bufferToSend += struct.pack('<I', 0x5a5a5a5a)
        bufferToSend += struct.pack('<I', 0xefbf5a5a)
        bufferToSend += struct.pack('<I', 0xbf5a5a5a)

        # Add the count of this packet, the size of the data it in (not counting padding) and the CRC.
        bufferToSend += struct.pack('<I', count)
        bufferToSend += struct.pack('<I', dataSize)
        bufferToSend += struct.pack('<I', crc)

        # Add the data
        print("\tDATA: Packet size:", len(packet))
        bufferToSend += packet

        # Send it to the printer
        SendBytes(bufferToSend)
        offset += packetSizeBytes
        count += 1

    print("Finish sending file. Finalizing...")
    SendTCPWithoutReading('\n')
    # Tell the printer that we have finished the file transfer
    return SendGCode(MachineCommands.EndWriteToSdCard)

# The equivalent of the js funciton crc32()
def crc32(data):
    crc = 0xffffffff
    for b in data:
        crc = crc ^ b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xedb88320
            else:
                crc = crc >> 1
    return crc ^ 0xffffffff

# def crc32(string):
#     value = 0xffffffffL
#     for ch in string:
#         value = table[(ord(ch) ^ value) & 0xff] ^ (value >> 8)

#     return -1 - value
