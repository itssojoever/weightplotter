import tkinter as tk
import csv
import os
import configparser
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator
from datetime import datetime
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox

#main
root = tk.Tk()
root.geometry("400x400")
root.title("Weightplotter")
root.iconname(None)
defaultSettings = {
    "legendtoggle" : "enabled",
    "legendloc" : "upper left",
    "filltoggle" : "enabled",
    "charttitle" : "Weight plot",
    "upperpadding" : 20,
    "lowerpadding" : 10,
    }
settingsExist = os.path.isfile("plotSettings.ini")
if not settingsExist:
    settingsConfig = configparser.ConfigParser()
    settingsConfig["Settings"] = defaultSettings
    with open("plotSettings.ini", "w") as plotSettingsFile:
        settingsConfig.write(plotSettingsFile)

#settings
def openSettings():
    settingsWindow = tk.Toplevel(root)
    settingsWindow.geometry("200x500")
    settingsWindow.title("Settings")
    settingsWindow.iconname(None)

    #Setting frames
    settingsFrame1 = ttk.LabelFrame(settingsWindow)
    settingFrames2 = ttk.LabelFrame(settingsWindow)
    settingFrames3 = ttk.LabelFrame(settingsWindow)
    settingFrames4 = ttk.LabelFrame(settingsWindow)
    settingFrame9999 = ttk.LabelFrame(settingsWindow)
    
    
    #Frame1
    settingsLabel1 = ttk.Label(settingsFrame1, text="Legend")
    legendOptionsList1 = ["enabled", "disabled"]
    legendOptionsList2 = ["best", "upper left", 
                          "lower left", "upper right",
                          "upper left", "right",
                          "center left", "center right",
                          "center", "upper center"]
    legendOptionsChoice2 = tk.StringVar(root)
    legendOptionsChoice1 = tk.StringVar(root)
    legendButton1 = tk.OptionMenu(settingsFrame1, legendOptionsChoice1, *legendOptionsList1)
    legendButton2 = tk.OptionMenu(settingsFrame1, legendOptionsChoice2, *legendOptionsList2)


    #Frame2
    chartTitleLabel1 = ttk.Label(settingFrames2, font="helvetica, 12", text="Input chart title:")
    chartTitleEntry1 = ttk.Entry(settingFrames2, font="helvetica, 12", justify="center")

    #Frame 3
    chartFillLabel1 = ttk.Label(settingFrames3, text="Enable or disable the fill between target and current:")
    chartOptionsList1 = ["enabled", "disabled"]
    chartOptionsChoice1 = tk.StringVar(root)
    chartFillOption1 = tk.OptionMenu(settingFrames3, chartOptionsChoice1, *chartOptionsList1)

    #Frame 4
    paddingLabel1 = ttk.Label(settingFrames4, text="Change upper padding:")
    paddingLabel2 = ttk.Label(settingFrames4, text="Change lower padding:")
    upperPaddingButton1 = ttk.Spinbox(settingFrames4, from_=3, to=100)
    lowerPaddingButton1 = ttk.Spinbox(settingFrames4, from_=-3, to=-100)

    
            

    #Frame???
    saveSettingsButton1 = ttk.Button(settingFrame9999, text="Save settings and close", command=lambda:saveSettings())

    #Grid
    #Frame1
    settingsFrame1.grid(row=0, column=0)
    settingsLabel1.grid(row=0, column=0)
    legendButton1.grid(row=1, column=0)
    legendButton2.grid(row=2, column=0)

    #Frame 2
    settingFrames2.grid(row=0, column=1)
    chartTitleLabel1.grid(row=0, column=0)
    chartTitleEntry1.grid(row=1, column=0)

    #Frame 3
    settingFrames3.grid(row=1, column=0)
    chartFillLabel1.grid(row=0, column=0)
    chartFillOption1.grid(row=1, column=0)

    #Frame 4
    settingFrames4.grid(row=2, column=0)
    paddingLabel1.grid(row=0, column=0)
    paddingLabel2.grid(row=2, column=0)
    upperPaddingButton1.grid(row=1, column=0)
    lowerPaddingButton1.grid(row=3, column=0)
    

    #Frame???
    settingFrame9999.grid(row=3, column=0)
    saveSettingsButton1.grid(row=0, column=0)

    if os.path.isfile("plotSettings.ini"):
        settingsReader = configparser.ConfigParser()
        settingsReader.read("plotSettings.ini")
        legendOptionsChoice1.set(settingsReader["Settings"]["legendtoggle"])
        legendOptionsChoice2.set(settingsReader["Settings"]["legendloc"])
        chartTitleEntry1.insert(0, settingsReader["Settings"]["charttitle"])
        chartOptionsChoice1.set(settingsReader["Settings"]["filltoggle"])
        upperPaddingButton1.set(settingsReader["Settings"]["upperpadding"])
        lowerPaddingButton1.set(settingsReader["Settings"]["lowerpadding"])

    def saveSettings():
        if os.path.isfile("plotSettings.ini"):
            with open("plotSettings.ini", "w") as settingsFile:
                settingsEditor = configparser.ConfigParser()
                settings = {
                    "legendtoggle" : legendOptionsChoice1.get(),
                    "legendloc" : legendOptionsChoice2.get(),
                    "filltoggle" : chartOptionsChoice1.get(),
                    "charttitle" : chartTitleEntry1.get(),
                    "upperpadding" : upperPaddingButton1.get(),
                    "lowerpadding" : lowerPaddingButton1.get(),
                    }
                settingsEditor["Settings"] = settings
                settingsEditor.write(settingsFile)


def loadData():
    if os.path.isfile("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        weightDesiredInput.insert(0, int(config["Configuration"]["desiredWeight"]))
        weightMeasurementInputted.set(config["Configuration"]["measurement"])
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
    
    #INI: target weight and preferred measurement
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
    configVerified = True #There isn't any use for this variable thus far, but it may serve a purpose at some point
    if os.path.isfile("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        verification = config["Configuration"]["measurement"]
        desired_weight_verification = config["Configuration"]["desiredweight"]
        if not desired_weight_verification.isdigit():
            messagebox.showerror(title="Error", message="Please use numbers only for target weight")
            weightDesiredInput.delete(0, tk.END)
            configVerified = False
            removeLastEntry("inputdata.csv")
        elif float(desired_weight_verification) <=30:
            messagebox.showwarning(title="Warning", message="Target weight cannot be too low!")
            configVerified = False
            removeLastEntry("inputdata.csv")
        if verification in {"kg", "lbs"}:
            pass
        else:
            messagebox.showerror(title="Error", message="Please complete all fields")
            configVerified = False
            removeLastEntry("inputdata.csv")
   
    inputVerified = True
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
                        inputVerified = False
                        removeLastEntry("inputdata.csv")

    if inputVerified == True and configVerified == True:
        messagebox.showinfo(title="Successful!", message="Entry successfully saved")

def removeLastEntry(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        contents = list(reader)
        contents.pop()
        with open(csv_file, 'w', newline='') as editFile:
            writer = csv.writer(editFile)
            writer.writerows(contents)

def viewPlot():   
    #plt.xkcd()
    plt.style.use("fivethirtyeight")
    if os.path.isfile("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        desiredWeight = int(config["Configuration"]["desiredweight"])
        measurement = config["Configuration"]["measurement"]
    
    if os.path.isfile("plotSettings.ini"):
        settingsReader = configparser.ConfigParser()
        settingsReader.read("plotSettings.ini")
        legendToggle = settingsReader["Settings"]["legendtoggle"]
        legendLoc = settingsReader["Settings"]["legendloc"]
        fillToggle = settingsReader["Settings"]["filltoggle"]
        chartTitle = settingsReader["Settings"]["charttitle"]
        upperYPadding = int(settingsReader["Settings"]["upperpadding"])
        lowerYPadding = int(settingsReader["Settings"]["lowerpadding"])

                                       
                                    

    else:
        pass
    if os.path.isfile("inputdata.csv"):
        data = pd.read_csv("inputdata.csv")
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        data.sort_index(inplace=True)
        data_resampled = data.resample("6D").mean()
        date = data_resampled.index
        weight_resampled = data_resampled["weight"]
        
    else:
        pass


    plt.figure(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, bottom=0.1)
    plt.plot(date, weight_resampled, label="Current weight")
    plt.axhline(y=desiredWeight, color="r", linestyle="-", alpha=0.15, label="Target weight")
    if fillToggle == "enabled":
        plt.fill_between(date, weight_resampled, desiredWeight,
                        where=(weight_resampled <= desiredWeight), 
                        interpolate=True,
                        alpha=0.25, color="red", label="Below goal")
    
    if legendToggle == "enabled":
        plt.legend(loc=legendLoc)

    #upperYPadding=0.1*desiredWeight
    reformulatedsubYPadding = weight_resampled.min() - lowerYPadding
    #plt.xticks(rotation=70)
    plt.ylim(reformulatedsubYPadding, desiredWeight + upperYPadding)
    plt.xlabel("Date")
    plt.ylabel(f"Weight in {measurement}")
    plt.title(chartTitle)

    plt.savefig('weightplot.png')
    plt.show()


#frames
Frame1 = ttk.LabelFrame(root)
Frame2 = ttk.LabelFrame(root)
Frame3 = ttk.LabelFrame(root)
Frame4 = ttk.LabelFrame(root)
Frame5 = ttk.LabelFrame(root)
Frame6 = ttk.LabelFrame(root)

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
l3 = ttk.Label(Frame3, font="helvetica, 12", text="Input target weight: ")
weightDesiredInput = ttk.Entry(Frame3, font="helvetica, 12")

#Frame4
l4 = ttk.Label(Frame4, font="Helvetica, 12", text="Input weight: ")
weightCurrentInput = ttk.Entry(Frame4, font="helvetica, 12")

#Frame5
saveButton = ttk.Button(Frame5, text="Save entry", command=lambda: saveData())
loadButton = ttk.Button(Frame5, text="Load settings", command=lambda: loadData())
viewVisualization = ttk.Button(Frame5, text="View visualization", command=lambda: viewPlot())
openSettingsButton = ttk.Button(Frame5, text="Edit plotting behaviour", command=lambda: openSettings())

#Frame6
#canvas1 = tk.Canvas(Frame6, width=1200, height=300)
#vizualisation = tk.PhotoImage(file="weightplot.png")
#canvas1.create_image(600, 20, image=vizualisation)
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
loadButton.grid(row=1, column=2)
viewVisualization.grid(row=1, column=3)
openSettingsButton.grid(row=1, column=4)

#Frame6
Frame6.grid(row=5, column=0)
#canvas1.grid(row=0, column=0)





root.mainloop()