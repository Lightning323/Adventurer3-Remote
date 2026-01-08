from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import machineCommands as server
from tkinter import filedialog
import os
import filamentCalc.filamentCalculator as fc

class FilePanel:
    def __init__(self, serverFrame):

        file = ttk.Label(serverFrame, text="Filament Calculator", font=("Helvetica", 9, "bold"))
        file.pack(anchor="w", pady=5)
        choose1 = ttk.Button(serverFrame, text="Launch Filament Calculator", command=self.openCalculator, width=35)
        choose1.pack(anchor="w", pady=5)

    def openCalculator(self):
        fc.FilamentCalculator()

        # # make a copy button
        # uploadAndPrint = tk.Frame(serverFrame)
        # uploadAndPrint.pack(anchor="w", pady=5, side='left')
        # instaButtonPad = 2

        # set event to selectFile()
        # choose1 = ttk.Button(
        #     uploadAndPrint, text="Choose a File", command=self.selectFile, width=35)
        # choose1.grid(row=0, column=0, padx=instaButtonPad,
        #              pady=instaButtonPad, columnspan=2)

        # self.file1 = ttk.Label(uploadAndPrint, text="", width=35)
        # self.file1.grid(row=1, column=0, padx=0, pady=2, columnspan=2)

        # upload = ttk.Button(
        #     uploadAndPrint, text="Upload to Printer", command=self.upload, width=17)
        # upload.grid(row=2, column=0, padx=0, pady=2)

        # uploadAndPrint = ttk.Button(
        #     uploadAndPrint, text="Upload and Print", command=self.uploadAndPrint, width=17)
        # uploadAndPrint.grid(row=2, column=1, padx=0, pady=2)

    # def _setOutput(self, output):
    #     output = output.replace("\r", "\n").replace("\n\n", "\n").strip()
    #     self.output.configure(text=output)

    # def welMsg(self, event):
    #     # if the textBox value is not empty, send the gcode to the server
    #     if self.textBox.get().strip() != "":
    #         print("Sending GCODE:", self.textBox.get())
    #         out = server.SendGCode(self.textBox.get())
    #         self._setOutput(out)
    #         self.textBox.delete(0, END)
    #     else:
    #         print("No GCODE to send")
    #         self.output.configure(text="No GCODE to send")
    #         self.textBox.delete(0, END)

 

    # def selectFile(self):
    #     # supported file formats are .gx and .gcode
    #     self.filename = filedialog.askopenfilename(
    #         initialdir="/", title="Select a File", filetypes=(("flashforge gcode files", "*.gx"),("gcode files", "*.gcode"),  ("all files", "*.*")))
    #     print("Selected File:", self.filename)
    #     self.file1.configure(text=self.filename)

    # def print(self,filename):
    #     print("STARTING PRINT...")
    #     out2 = server.PrintFile(filename)
    #     print(out2)
    #     self._setOutput(out2)

    # def uploadAndPrint(self):
    #     # create a variable with the filename without the path
    #     printerFileName = os.path.basename(self.filename)

    #     out = server.StoreFile(self.filename, printerFileName)
    #     print(out)

    #     print("STARTING PRINT...")
    #     out2 = server.PrintFile(printerFileName)
    #     print(out2)
    #     self._setOutput(out+"\n"+out2)

    # def upload(self):
    #     # create a variable with the filename without the path
    #     printerFileName = os.path.basename(self.filename)
    #     out = server.StoreFile(self.filename, printerFileName)
    #     print(out)
    #     self._setOutput(out)
