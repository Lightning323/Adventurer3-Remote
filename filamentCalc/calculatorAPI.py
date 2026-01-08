import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import ttk

def header(root, text):
    label = Label(root, text=text, font=("Helvetica", 10, "bold"))
    label.pack()
    return label

def createRootWindow(title):
    root = Tk()
    # set the window style to xpadmin
    s = ttk.Style()
    s.theme_use('xpnative')

    root.title(title)
    root.config(padx=10, pady=10)
    root.resizable(0, 0)
    return root

def set_width(window, width):
    window.geometry("{}x{}".format(width, window.winfo_height()))

class PopupWindow():
    def __init__(self, title, body):
        self.root = tk.Tk()
        ttk.Style().theme_use('xpnative')
        self.root.title(title)
        self.root.config(padx=25, pady=10)
        # make this one bolded
        self.lt = ttk.Label(self.root, text=title,
                            font=("Helvetica", 9, 'bold'))
        self.lt.pack()

        self.l = ttk.Label(self.root, text=body)
        self.l.pack()
        self.b = ttk.Button(self.root, text="OK", command=self.cleanup)
        self.b.pack(padx=5, pady=10)
        self.root.resizable(0, 0)
        # if self.root.winfo_width() < 300:
        #     set_width(self.root, 300)
        # elif self.root.winfo_width() > 600:
        #     set_width(self.root, 600)
        self.root.mainloop()

    def cleanup(self):
        self.root.destroy()


class OutputBox:
    def __init__(self, grid, txt, row, width=20):
        self.label = Label(grid, text=txt+":")
        self.label.grid(row=row, column=0, sticky=W, padx=5, pady=5)

        #set background color to white
        self.entry = Label(grid, text="", width=width, borderwidth=0, relief="solid", background="white")
        self.entry.grid(row=row, column=1, sticky=W, padx=5, pady=5)

        #add a copy button to the right of the entry
        self.copyButton = ttk.Button(grid, text="Copy", command=self.copy, width=6)
        self.copyButton.grid(row=row, column=2, sticky=W, padx=5, pady=5)
        self.value = ""

    def setValue(self, value):
        self.entry.config(text=value)
        self.value = value

    def copy(self): #copy the value to the clipboard
        self.entry.clipboard_clear()
        self.entry.clipboard_append(self.value)



class InputBox:
    def __init__(self, grid, txt, row, width=20, onchangeEvent = None):
        self.label = Label(grid, text=txt+":")
        self.label.grid(row=row, column=0, sticky=W, padx=5, pady=5)

        self.entry = ttk.Entry(grid, width = width)
        self.entry.grid(row=row, column=1, padx=5, pady=5)
        if onchangeEvent:
            self.entry.bind('<Return>', onchangeEvent)

    def getValue(self):
        val = self.entry.get().strip()
        if not val:
            self.entry.delete(0, END)
            self.entry.insert(0, 0)
            return 0
        else:
            try:
                return float(val)
            except ValueError:
                self.entry.delete(0, END)
                self.entry.insert(0, 0)
                return 0

    def getValueAsString(self):
        return self.entry.get().strip()

    def setValue(self,value):
        self.entry.delete(0, END)
        self.entry.insert(0, value)

