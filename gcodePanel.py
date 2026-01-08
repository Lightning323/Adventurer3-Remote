from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import machineCommands as server
from tkinter import filedialog
import os


class GcodePanel:
    def __init__(self, serverFrame):
        textBoxLabel = ttk.Label(
            serverFrame, text="Control Panel:", font=("Helvetica", 9, "bold"))
        textBoxLabel.pack(anchor="w", pady=10)
        self.textBox = ttk.Entry(serverFrame, width=42)
        self.textBox.bind('<Return>', self.welMsg)
        self.textBox.pack(anchor="w")
        self.ledOn = True

        gcodeButtonFrame = tk.Frame(serverFrame)

        instaButtonPad = 2
        buttonWidth = 20

        # create a button for stopping the printerServer
        self.getEndstopStatusButton = ttk.Button(
            gcodeButtonFrame, text="Get Endstop Status", command=self.getEndstopStatus, width=buttonWidth)
        self.getEndstopStatusButton.grid(
            row=0, column=0)

        self.getFirmwareVersionButton = ttk.Button(
            gcodeButtonFrame, text="Get Firmware Info", command=self.getFirmwareVersion, width=buttonWidth)
        self.getFirmwareVersionButton.grid(
            row=0, column=1)

        self.stopPrintingButton = ttk.Button(
            gcodeButtonFrame, text="Stop Printing", command=self.stopPrinting, width=buttonWidth)
        self.stopPrintingButton.grid(
            row=1, column=0)

        self.pausePrintingButton = ttk.Button(
            gcodeButtonFrame, text="Pause Printing", command=self.pausePrinting, width=buttonWidth)
        self.pausePrintingButton.grid(
            row=1, column=1)

        self.resumePrintingButton = ttk.Button(
            gcodeButtonFrame, text="Resume Printing", command=self.resumePrinting, width=buttonWidth)
        self.resumePrintingButton.grid(
            row=2, column=0)

        self.offLedButton = ttk.Button(
            gcodeButtonFrame, text="Led Off", command=self.toggleLed, width=buttonWidth)
        self.offLedButton.grid(
            row=2, column=1)

        self.emergencyStopButton = ttk.Button(
            gcodeButtonFrame, text="Emergency Stop", command=self.emergencyStop, width=buttonWidth)
        self.emergencyStopButton.grid(
            row=3, column=0)

        self.getPositionButton = ttk.Button(
            gcodeButtonFrame, text="Get Position", command=self.getPosition, width=buttonWidth)
        self.getPositionButton.grid(
            row=3, column=1)

        self.activateBackFanButton = ttk.Button(
            gcodeButtonFrame, text="Activate Back Fan", command=self.activateBackFan, width=buttonWidth)
        self.activateBackFanButton.grid(
            row=4, column=0)

        self.deactivateBackFanButton = ttk.Button(
            gcodeButtonFrame, text="Deactivate Back Fan", command=self.deactivateBackFan, width=buttonWidth)
        self.deactivateBackFanButton.grid(
            row=4, column=1)

        self.activateFanButton = ttk.Button(
            gcodeButtonFrame, text="Activate Nozzle Fan", command=self.activateFan, width=buttonWidth)
        self.activateFanButton.grid(
            row=5, column=0)

        self.deactivateFanButton = ttk.Button(
            gcodeButtonFrame, text="Deactivate Nozzle Fan", command=self.deactivateFan, width=buttonWidth)
        self.deactivateFanButton.grid(
            row=5, column=1)


        # #Create a Label
        # self.output2 = ttk.Label(gcodeButtonFrame, text="", font=("Helvetica", 9, "bold"))
        # self.output2.grid(row=6, column=0, columnspan=2)
        # self.printFileButton = ttk.Button(
        #     gcodeButtonFrame, text="Print File", command=self.printFile, width=buttonWidth)
        # self.printFileButton.grid(
        #     row=9, column=0)
        # self.setNozzlePositionButton = ttk.Button(
        #     gcodeButtonFrame, text="Set Nozzle Position", command=self.setNozzlePosition, width=buttonWidth)
        # self.setNozzlePositionButton.grid(
        #     row=9, column=1)


        gcodeButtonFrame.pack(anchor="w", pady=2)

        self.output = ttk.Label(serverFrame, text="GCODE Output will appear here.\n\n",
                                borderwidth=1, relief="solid", width=40, background="#ddd")
        self.output.pack(anchor="w", pady=5)

        # make a copy button
        copyButton = ttk.Button(
            serverFrame, text="Copy Output", command=self.copy, width=15)
        copyButton.pack(anchor="w")

        f2 = ttk.Label(serverFrame)
        f2.pack(anchor="w", pady=5)

    def _setOutput(self, output):
        output = output.replace("\r", "\n").replace("\n\n", "\n").strip()
        self.output.configure(text=output)

    def welMsg(self, event):
        # if the textBox value is not empty, send the gcode to the server
        if self.textBox.get().strip() != "":
            print("Sending GCODE:", self.textBox.get())
            out = server.SendGCode(self.textBox.get())
            self._setOutput(out)
            self.textBox.delete(0, END)
        else:
            print("No GCODE to send")
            self.output.configure(text="No GCODE to send")
            self.textBox.delete(0, END)

    def copy(self):
        self.output.clipboard_clear()
        self.output.clipboard_append(self.output.cget("text"))
        print("Copied to clipboard")

    def getEndstopStatus(self):
        self._setOutput(server.GetPrinterStatus())

    def getFirmwareVersion(self):
        self._setOutput(server.GetFirmwareVersion())

    def getTemperature(self):
        self._setOutput(server.GetTemperature())

    def stopPrinting(self):
        self._setOutput(server.StopPrinting())

    def pausePrinting(self):
        self._setOutput(server.PausePrinting())

    def resumePrinting(self):
        self._setOutput(server.ResumePrinting())

    def toggleLed(self):
        if(self.ledOn):
            self._setOutput(server.DisableLED())
            self.ledOn = False
            self.offLedButton.configure(text="Led On")
        else:
            self._setOutput(server.EnableLED())
            self.ledOn = True
            self.offLedButton.configure(text="Led Off")

    
    def emergencyStop(self):
        self._setOutput(server.EmergencyStop())

    def activateBackFan(self):
        self._setOutput(server.ActivateBackFan())

    def deactivateBackFan(self):
        self._setOutput(server.DeactivateBackFan())

    def activateFan(self):
        self._setOutput(server.SendGCode("M106 P0  S120"))

    def deactivateFan(self):
        self._setOutput(server.SendGCode("M107 P0"))

    def getPosition(self):
        self._setOutput(server.GetPosition())
        
    def home(self):
        self._setOutput(server.SendGCode("G1 X0 Y0 Z0 F1000"))

    def printFile(self):
        self.textBox.delete(0, END)
        #Set textbox value to the gcode value
        self.textBox.insert(0, 'M23 0:/user/<filename>')
    
    def setNozzlePosition(self):
        self.textBox.delete(0, END)
        #Set textbox value to the gcode value
        self.textBox.insert(0, 'G1 X<x pos> Y<y pos> Z<z pos> E<extruder> F2000')

    def setIsPrinting(self, isPrinting):
        if isPrinting:
            self.resumePrintingButton.configure(state="enabled")
            self.pausePrintingButton.configure(state="enabled")
            self.stopPrintingButton.configure(state="enabled")
        else:
            self.resumePrintingButton.configure(state="disabled")
            self.pausePrintingButton.configure(state="disabled")
            self.stopPrintingButton.configure(state="disabled")

