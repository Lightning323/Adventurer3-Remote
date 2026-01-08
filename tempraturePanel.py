from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import machineCommands as server
from tkinter import filedialog
import os
import threading
import time


class TempraturePanel:
    def __init__(self, serverFrame):
        textBoxLabel = ttk.Label(serverFrame, text="Set Temprature:", font=("Helvetica", 9, "bold"))
        textBoxLabel.pack(anchor="w", pady=5)

        tempFrame = tk.Frame(serverFrame)
        tempFrame.pack(anchor="w", pady=10)

        nozzle = ttk.Label(tempFrame, text="Nozzle:")
        nozzle.grid(row=0, column=0, sticky="w")

        self.nozzleSet = ttk.Entry(tempFrame, width=20)
        self.nozzleSet.bind('<Return>', self.setNozzleTemp)
        self.nozzleSet.grid(row=0, column=1, sticky="w",padx=5,pady=5)

        bed = ttk.Label(tempFrame, text="Buildplate:")
        bed.grid(row=1, column=0, sticky="w")

        self.bedSet = ttk.Entry(tempFrame, width=20)
        self.bedSet.bind('<Return>', self.setBedTemp)
        self.bedSet.grid(row=1, column=1, sticky="w",padx=5,pady=5)
        self.nozzleSet.insert(0, "0")
        self.bedSet.insert(0, "0")

        realTemp = ttk.Label(serverFrame, text="Actual Temprature:", font=("Helvetica", 9, "bold"))
        realTemp.pack(anchor="w", pady=5)

        realTempFrame = tk.Frame(serverFrame)
        realTempFrame.pack(anchor="w", pady=10)

        a = ttk.Label(realTempFrame, text="Nozzle:", width=10)
        a.grid(row=0, column=0, sticky="w")

        b = ttk.Label(realTempFrame, text="Buildplate:", width=10)
        b.grid(row=1, column=0, sticky="w")

        self.realNozzle = ttk.Label(realTempFrame, text="--℃")
        self.realNozzle.grid(row=0, column=1, sticky="w")

        self.realBed = ttk.Label(realTempFrame, text="--℃")
        self.realBed.grid(row=1, column=1, sticky="w")

        nozzleSlash = ttk.Label(realTempFrame, text="/")
        nozzleSlash.grid(row=0, column=2, sticky="w",padx=5)

        bedSlash = ttk.Label(realTempFrame, text="/")
        bedSlash.grid(row=1, column=2, sticky="w",padx=5)

        self.targetNozzle = ttk.Label(realTempFrame, text="--℃")
        self.targetNozzle.grid(row=0, column=3, sticky="w")

        self.targetBed = ttk.Label(realTempFrame, text="--℃")
        self.targetBed.grid(row=1, column=3, sticky="w")

        #start temprature update thread on a separate thread
        self.updateTempThread = threading.Thread(target=self.getTemprature)
        self.updateTempThread.start()

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

    def setNozzleTemp(self, event):
        if(not self.nozzleSet.get().isdigit()):
            print("Bed temperature must be an integer")
            #set the bedSet.get to 0
            self.nozzleSet.delete(0, END)
            self.nozzleSet.insert(0, "0")
            return
        print("Setting nozzle temperature to:", self.nozzleSet.get())
        server.SetNozzleTemperature(int(self.nozzleSet.get()))

    def setBedTemp(self, event):
        #make sure the bedSet.get is an int
        if(not self.bedSet.get().isdigit()):
            print("Bed temperature must be an integer")
            #set the bedSet.get to 0
            self.bedSet.delete(0, END)
            self.bedSet.insert(0, "0")
            return
        print("Setting bed temperature to:", self.bedSet.get())
        server.SetBedTemperature(int(self.bedSet.get()))


    #a function that gets the temprature using server.getTemprature() and updates the labels
    def getTemprature(self):
        while True:
            try:
                tempInfo = server.GetTemperature()
                try:
                    tempInfo = tempInfo.split("\n")[1]
                    nozzle1 = tempInfo.split(" ")[0].split(":")[1]
                    bed1 = tempInfo.split(" ")[1].split(":")[1]
                    self.nozzleTemp = int(nozzle1.split("/")[0])
                    self.nozzleGoal = int(nozzle1.split("/")[1])
                    self.bedTemp = int(bed1.split("/")[0])
                    self.bedGoal = int(bed1.split("/")[1])
                    self.realNozzle.configure(text=str(self.nozzleTemp) + "℃")
                    self.realBed.configure(text=str(self.bedTemp) + "℃")
                    self.targetNozzle.configure(text=str(self.nozzleGoal) + "℃")
                    self.targetBed.configure(text=str(self.bedGoal) + "℃")
                except:
                    print("Temprature parsing error...")
            except:
                print("Temprature reading error...")

            time.sleep(5)

#Gcode buttons with parameters
    def SetNozzleTemperature(self):
        self.textBox.delete(0, END)
        #Set textbox value to the gcode value
        self.textBox.insert(0, 'M104 S<temp> T0')

    def SetBedTemperature(self):
        self.textBox.delete(0, END)
        #Set textbox value to the gcode value
        self.textBox.insert(0, 'M140 S<temp> T0')