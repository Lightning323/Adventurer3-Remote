import tkinter as tk
import tkinter.ttk as ttk


def set_width(window, width):
    window.geometry("{}x{}".format(width, window.winfo_height()))


class WarningWindow():
    def __init__(self, path, title, body, windowGeometryX = None, windowGeometryY = None):
        self.root = tk.Tk()
        ttk.Style().theme_use('xpnative')
        self.root.title(title)

        self.root.config(padx=25, pady=10)
        self.root.iconbitmap(path + "/resources/icon.ico")

        if(windowGeometryX != None or windowGeometryY != None):
            self.root.geometry("{}x{}".format(windowGeometryX, windowGeometryY))
        self.lt = ttk.Label(self.root, text=title,
                            font=("Helvetica", 12, 'bold'))
        #set the label to red highlight the text
        # self.lt.config(background="yellow", foreground="black")
        self.lt.pack(pady=10)

        self.l = ttk.Label(self.root, text=body)
        self.l.pack()
        self.b = ttk.Button(self.root, text="OK", command=self.cleanup)
        self.b.pack(padx=5, pady=10)
        self.root.resizable(0, 0)
        self.root.lift()
        self.root.attributes('-topmost',True)
        self.root.after_idle(self.root.attributes,'-topmost',True)

        self.root.mainloop()

        
    def cleanup(self):
        self.root.destroy()

class PopupWindow():
    def __init__(self, path, title, body, stayOnTop = False, windowGeometryX = None, windowGeometryY = None):
        self.root = tk.Tk()
        ttk.Style().theme_use('xpnative')
        self.root.title(title)
        self.root.config(padx=25, pady=10)
        self.root.iconbitmap(path + "/resources/icon.ico")

        if(windowGeometryX != None or windowGeometryY != None):
            self.root.geometry("{}x{}".format(windowGeometryX, windowGeometryY))

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
        self.root.lift()
        self.root.attributes('-topmost',True)

        if(stayOnTop):
            self.root.after_idle(self.root.attributes,'-topmost',True)
        else:
            self.root.after_idle(self.root.attributes,'-topmost',False)

        self.root.mainloop()

    def cleanup(self):
        self.root.destroy()
