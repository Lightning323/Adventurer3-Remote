from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import machineCommands as server
from tkinter import filedialog
import os
import cv2
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#TODO: Print the printer status somewhere within the software and hide the gcode button.

model = tf.keras.Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

path = os.path.dirname(os.path.abspath(__file__))
model.load_weights(path+'\\resources\\model.h5')

def getWarningLevel(img):
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis
    img_array = tf.image.resize(img_array, (128, 128))
    img_array = tf.cast(img_array, tf.float32) / 255.0
    predictions = model.predict(img_array)
    return predictions[0][1]


# import matplotlib.pyplot as plt
# cap = cv2.VideoCapture("http://192.168.0.130:8080/?action=stream")
# ret, img = cap.read()
# cap.release()
# plt.imshow(img)
# plt.show()
# print(getWarningLevel(img))


class ClassifierPanel:
    def __init__(self, bottomFrame):
        #semibold the text field
        self.classValue = "PRINTING"
        self.recording = False
        #get working directory
        self.path = os.path.dirname(os.path.abspath(__file__))
        textBoxLabel0 = ttk.Label(bottomFrame, text="Image Classification:",font=("Helvetica", 9, "bold"))
        textBoxLabel0.grid(row=0, column=0,columnspan=2, sticky="w")

        leftFrame1 = tk.Frame(bottomFrame)
        leftFrame1.grid(row=1, column=0)

        rightFrame1 = tk.Frame(bottomFrame)
        rightFrame1.grid(row=1, column=1)

        self.record = ttk.Checkbutton(leftFrame1, text="Record", command=self.record, width=15)
        #set record to unchecked
        self.record.state(['!alternate'])
        self.record.pack(anchor="w",padx=5, pady=5)

        self.info1 = ttk.Label(leftFrame1, text="")
        self.info1.pack(anchor="w")
        self.info1.config(text="Ok: "+str(len(os.listdir(self.path+"\\resources\\classes\\PRINTING")))+\
                    ",\nFail: "+str(len(os.listdir(self.path+"\\resources\\classes\\WARNING"))))

        s = ttk.Style()
        #set the hovered background color to red
        s.configure("activated.TButton", background="#22aaff")

        self.button1 = ttk.Button(rightFrame1, text="Ok", command=self.printing, width=15)
        self.button1.pack(anchor="w")
        self.button1.config(style="activated.TButton")

        self.button2 = ttk.Button(rightFrame1, text="Warning / Fail", command=self.warning, width=15)
        self.button2.pack(anchor="w")
    
    def printing(self):
        self.classValue = "PRINTING"
        print("Printing")
        self.button1.config(style="activated.TButton")
        # self.button.config(style="TButton")
        self.button2.config(style="TButton")

    def warning(self):
        self.classValue = "WARNING"
        print("Warning / Fail")
        self.button2.config(style="activated.TButton")
        # self.button.config(style="TButton")
        self.button1.config(style="TButton")

    def record(self):
        self.recording = not self.recording
        print("Recording: " + str(self.recording))

    def saveImage(self,image):
        if(self.recording):
            #image name = current time in microseconds
            imgName = str(int(round(time.time() * 1000)))
            path = self.path+"\\resources\\classes\\"+str(self.classValue)+"\\img "+imgName+".jpg"
            print("SAVING TO "+path)
            cv2.imwrite(path, image)
            print("Saved image")
            #update info1 with the files in each directory
            self.info1.config(text="Ok: "+str(len(os.listdir(self.path+"\\resources\\classes\\PRINTING")))+\
                    ",\nFail: "+str(len(os.listdir(self.path+"\\resources\\classes\\WARNING"))))