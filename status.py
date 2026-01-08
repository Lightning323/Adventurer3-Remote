import machineCommands as server
import time
import threading

'''
Endstop: X-max:1 Y-max:0 Z-max:0
MachineStatus: READY
MoveMode: READY
Status: S:1 L:0 J:0 F:0
LED: 1
CurrentFile:
'''

class Status:
    def __init__(self):
        self.updateTempThread = threading.Thread(target=self.getStatus)
        self.updateTempThread.start()
        self.printing = False


    def getStatus(self):
        while True:
            tempInfo = server.GetPrinterStatus().split("\n")
            if(tempInfo[5].split(":")[1].strip() == ''):
                self.printing = False
            else:
                self.printing = True
            print("printing: " + str(self.printing))
            time.sleep(5)