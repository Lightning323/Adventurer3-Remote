import cv2
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from PIL import Image
from PIL import ImageTk
import threading
import time
import os
import messageWindow as msg
import machineCommands as server

path = os.path.dirname(os.path.abspath(__file__))
# print("WORKING DIRECTORY: " + path)

ipAdressFilePath = path + "\\resources\\ipAdress.txt"


def loadIPAdress():
    global ipAdress
    file = open(ipAdressFilePath, "r")
    ipAdress = file.read()
    file.close()


def setIpAdress(ip):
    global ipAdress
    ipAdress = ip
    file = open(ipAdressFilePath, "w")
    file.write(ip)
    file.close()


loadIPAdress()
print("Current IP Adress: "+ipAdress+".")

keepIP = input("Do you want to keep this IP Adress? (Y/n) ").lower().strip()
if keepIP == "n":
    ipAdress = input("Enter new IP Adress: ").strip()
    setIpAdress(ipAdress)
    print("IP Adress changed to: "+ipAdress+".")


conencted = False


print(f"Connecting to printer... IP: {ipAdress}\n")
conencted = server.Connect(ipAdress)

imageInfo = None
classifyToggleButton = None
continueCameraFeed = True


def startCamera():
    print("STARTING CAMERA FEED...")
    a = cap = cv2.VideoCapture('http://'+ipAdress+':8080/?action=stream')
    frameWorking = True

    def show_frame():
        try:
            if(continueCameraFeed):
                _, frame = cap.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                frameWorking = True
                imageScale = 1
                cv2image = cv2.resize(cv2image, (640, 480))
                updateWindowImage(cv2image)
                # if(classifyImages):
                #     classifyImage(frame)
        except cv2.error as e:
            print("Error: " + str(e))
            # show error message
            if(frameWorking):
                window = msg.PopupWindow(path, "Error Connecting to Camera", "Could not connect to Adventurer 3 Camera.\n\
                    Please check that your camera is enabled and the IP address is correct.")
                frame = np.zeros((480, 640, 3), np.uint8)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                updateWindowImage(cv2image)
            frameWorking = False
        if(continueCameraFeed):
            delay = 300
            # if(classifyImages):
            #     delay = 1000
            lmain.after(delay, show_frame)

    threading.Timer(1.0, show_frame).start()


def resetCamera():
    print("RESETTING CAMERA...")
    continueCameraFeed = False
    time.sleep(2.5)
    continueCameraFeed = True
    startCamera()


if(conencted):
    classifyImages = True
    root = tk.Tk()
    s = ttk.Style()
    s.theme_use('xpnative')
    root.title("Adventurer 3 3D Printer App")
    root.config(padx=10, pady=10)
    root.iconbitmap(path + "/resources/icon.ico")
    root.resizable(0, 0)

    imageFrame = tk.Frame(root)
    imageFrame.grid(row=0, column=0, pady=0)
    infoFrame = tk.Frame(imageFrame)
    infoFrame.pack(anchor="w")

    ipAdressLabel = tk.Label(infoFrame, text="IP Adress: ")
    ipAdressLabel.grid(row=0, column=0)

    def keepIPViaGUI(arg):
        ipAdress = ipAdressTextBox.get()
        print("IP Adress: " + ipAdress)
        setIpAdress(ipAdress)
        msg.PopupWindow(path, "IP Adress Changed",
                        "Please restart the app for the changes to take effect.")

    ipAdressTextBox = ttk.Entry(infoFrame, width=15)
    ipAdressTextBox.insert(0, ipAdress)
    ipAdressTextBox.bind('<Return>', keepIPViaGUI)
    ipAdressTextBox.grid(row=0, column=1)

    imageInfo = tk.Label(infoFrame, text="")
    resetCameraButton = ttk.Button(
        infoFrame, text="Reset Camera Feed", command=resetCamera)

    imageInfo.grid(row=0, column=2, padx=15)
    resetCameraButton.grid(row=0, column=3, padx=15)

    lmain = tk.Label(imageFrame)
    lmain.pack()

    bottomFrame = tk.Frame(imageFrame)
    bottomFrame.pack(side='bottom', anchor="w", padx=5, pady=5)

    leftFrame = tk.Frame(bottomFrame)
    leftFrame.grid(row=0, column=0, padx=10, pady=10)
    import classifierPanel as classifier
    classifierPanel = classifier.ClassifierPanel(leftFrame)

    tempFrame = tk.Frame(bottomFrame)
    tempFrame.grid(row=0, column=1, padx=10, pady=10)
    import filePanel
    fp = filePanel.FilePanel(tempFrame)

    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1, padx=6, pady=10)

    import gcodePanel as gcode
    gc = gcode.GcodePanel(rightFrame)
    import tempraturePanel as temprature
    temp = temprature.TempraturePanel(rightFrame)

    warningMode = True

    def classifyImage(imageFrame):
        global warningMode
        # print("Classifying Image. Bed goal: "+str(temp.bedGoal))

        if(temp.bedGoal > 0):
            gc.setIsPrinting(True)
            prediction = classifier.getWarningLevel(imageFrame)
            failConfidence = round(prediction*100, 2)

            if(failConfidence > 80):
                errorMsg = "WARNING!"
                if(warningMode):
                    msg.WarningWindow(
                        path, "PRINT WARNING!", "Possible print failure!\nConfidence: " + str(failConfidence) + "%", 400, 170)
                    warningMode = False
            else:
                warningMode = True

            imageInfo.config(text="Error confidence: " +
                             str(failConfidence)+"%    ")
        else:
            imageInfo.config(text="Not printing...")
            warningMode = True
            gc.setIsPrinting(False)

    def updateWindowImage(cv2image):
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        classifierPanel.saveImage(cv2image)

    def clearWindowImage():
        frame = np.zeros((480, 640, 3), np.uint8)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        updateWindowImage(cv2image)
    # create a blank screen

    print("STARTING APPLICATION...")
    clearWindowImage()
    startCamera()
    root.mainloop()

else:
    window = msg.PopupWindow(path, "Error Connecting",
                             "Could not connect to the 3D Printer")
