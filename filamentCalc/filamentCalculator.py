# create a new tkinter window
from tkinter import *
from tkinter import ttk
import filamentCalc.calculatorAPI as calc

class FilamentCalculator:

    def __init__(self):
        root = calc.createRootWindow("Calculator")
        label = calc.header(root, text="Filament Calculator")
        label.pack()

        grid = Frame(root)
        grid.pack()

        self.weight = calc.InputBox(grid, "Filament Weight (grams)",0)
        
        self.totalweight = calc.InputBox(grid, "Total Filament Weight (grams)",1)
        self.totalweight.setValue(1000)
        self.cost = calc.InputBox(grid, "Filament Total Cost",2)
        self.cost.setValue(22.00)

        self.outPercentOfWeight = calc.OutputBox(grid, "% of Weight",3)
        self.outCost = calc.OutputBox(grid, "Cost",4)

        button = ttk.Button(root, text="Calculate", command=self.calculate)
        #make the buttons width, fill the window width
        button.pack(pady=5, fill=X)
        root.mainloop()

    def calculate(self):
        weight = self.weight.getValue()
        cost = self.cost.getValue()
        totalweight = self.totalweight.getValue()
        if weight == 0:
            calc.PopupWindow("Error", "Please enter a valid weight.")
            return
        if cost == 0:
            calc.PopupWindow("Error", "Please enter a valid cost.")
            return


        percentOfWeight = round( (weight/totalweight) ,3)
        cost = round(cost * percentOfWeight,2)

        self.outPercentOfWeight.setValue(str(percentOfWeight*100)+"%")
        self.outCost.setValue("$"+str(cost))