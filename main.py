import tkinter as tk
import csv
import os
import configparser
from datetime import datetime
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox

root = tk.Tk()
root.geometry("400x400")
root.title("Weightplotter")
root.iconname(None)

def loadData():
    if os.path.isfile("config.ini"):
        pass
    else:
        with open("config.ini", "w") as f:
            pass

def saveData():
    #CSV: current date and current weight
    inputtedDate = cal.get_date()
    inputtedCurrentWeight = weightCurrentInput.get()

    columnsExist = os.path.isfile("inputdata.csv")
    
    with open("inputdata.csv", "a", newline="") as csvfile:
        columns = ["date", "weight"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        if not columnsExist:
            writer.writeheader()
        writer.writerow({"date": inputtedDate, "weight": inputtedCurrentWeight})
        csvfile.close()
    
    #INI: desired weight and preferred measurement
    inputtedMeasurement = weightMeasurementInputted.get()
    desiredWeight = weightDesiredInput.get()

    configuration = {
        "measurement" : inputtedMeasurement,
        "desiredWeight" : desiredWeight
    }
    config = configparser.ConfigParser()
    config["Configuration"] = configuration
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    verifyFields()

def verifyFields():
    #config.ini
    configVerified = 1
    if os.path.isfile("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        verification = config["Configuration"]["measurement"]
        desired_weight_verification = config["Configuration"]["desiredweight"]
        if verification in {"kg", "lbs"} and len(desired_weight_verification)>1:
           pass
        else:
            configVerified = 0
            messagebox.showerror(title="Error", message="Please complete all fields")
    if configVerified == 1:
        pass
    else:
        pass
    #inputdata.csv
    inputVerified = 1
    if os.path.isfile("inputdata.csv"):
        with open("inputdata.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if len(row) == 2:
                    weight_value = row["weight"]
                    try:
                        weight_value = float(weight_value)
                    except ValueError:
                        messagebox.showerror(title="Error", message="Please use numbers only for weight")
                        removeLastEntry("inputdata.csv")

def removeLastEntry(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        contents = list(reader)
        contents.pop()
        with open(csv_file, 'w', newline='') as editFile:
            writer = csv.writer(editFile)
            writer.writerows(contents)

   
        
                        
    # if os.path.isfile("inputdata.csv") and len("inputdata.csv")>1:
    #     csvExists = 1
    
    # if configVerified == 1 and csvExists == 1:
    #     messagebox.showinfo(title="Saved", message="Data saved successfully")
    # else:
    #     messagebox.showerror(title="Error", message="Error: Data not saved")


#frames
Frame1 = ttk.LabelFrame(root)
Frame2 = ttk.LabelFrame(root)
Frame3 = ttk.LabelFrame(root)
Frame4 = ttk.LabelFrame(root)
Frame5 = ttk.LabelFrame(root)

#Calendar function
currentDate = datetime.now()
currentDay = currentDate.day
currentMonth = currentDate.month
currentYear = currentDate.year

cal = Calendar(Frame1, selectmode = "day", 
               year = currentYear, 
               month = currentMonth, 
               day = currentDay)

#Frame1
l1 = ttk.Label(Frame1, font="helvetica, 12", text="Select the date: ")

#Frame2
l2 = ttk.Label(Frame2, font="helvetica, 12", text="Select weight measurement: ")
weightoption_list = ["kg", "lbs"]
weightMeasurementInputted = tk.StringVar(root)
weightMeasurementInputted.set("Select a measurement")
weightMeasurementOption = tk.OptionMenu(Frame2, weightMeasurementInputted, *weightoption_list)

#Frame3
l3 = ttk.Label(Frame3, font="helvetica, 12", text="Input desired weight: ")
weightDesiredInput = ttk.Entry(Frame3, font="helvetica, 12")

#Frame4
l4 = ttk.Label(Frame4, font="Helvetica, 12", text="Input weight")
weightCurrentInput = ttk.Entry(Frame4, font="helvetica, 12")

#Frame5
saveButton = ttk.Button(Frame5, text="Save data", command=lambda: saveData())

#gridding/packing ---------

#Frame1
Frame1.grid(row=0, column=0)
l1.grid(row=0, column=0)
cal.grid(row=0, column=1)

#Frame2
Frame2.grid(row=1, column=0)
l2.grid(row=0, column=0)
weightMeasurementOption.grid(row=0, column=1)

#Frame3
Frame3.grid(row=2, column=0)
l3.grid(row=0, column=0)
weightDesiredInput.grid(row=0, column=1)

#Frame4
Frame4.grid(row=3, column=0)
l4.grid(row=0, column=0)
weightCurrentInput.grid(row=0, column=1)

#Frame5
Frame5.grid(row=4, column=0)
saveButton.grid(row=1, column=1)





root.mainloop()