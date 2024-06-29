import tkinter as tk
import csv
import os
import configparser
import pandas as pd
import ttkbootstrap as ttk
import matplotlib.ticker as ticker
from matplotlib import pyplot as plt
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
#from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog

#main
root = ttk.Window(themename="superhero")
root.position_center()
root.resizable(False, False)
root.geometry("965x450")
root.title("Weightplotter")
root.iconname(None)
defaultSettings = {
    "legendtoggle" : "enabled",
    "legendloc" : "upper left",
    "filltoggle" : "enabled",
    "fillalpha" : 25,
    "charttitle" : "Weight plot",
    "upperpadding" : 20,
    "lowerpadding" : 3,
    "linewidth" : 3,
    #"weightlinecolour" : "#56c91c",
    #"calorieslinecolour" : "#ab0f1c",
    #"alphalinecolour" : "#e02232",
    #"targetweightlinecolour" : "#073ae0",
    }
settingsExist = os.path.isfile("plotSettings.ini")
if not settingsExist:
    settingsConfig = configparser.ConfigParser()
    settingsConfig["Settings"] = defaultSettings
    with open("plotSettings.ini", "w") as plotSettingsFile:
        settingsConfig.write(plotSettingsFile)

#settings
def openSettings():

    def slider(e):
        fillScaleLabel2.config(text=f"Current opacity: {int(fillScale1.get())}%")

    # def colourChooser(button):
    #     global weightColour #This is bad practice; will refactor when more experienced and can work it out
    #     global caloriesColour
    #     global alphaColour
    #     global targetWeightColour

    #     if button == "weight":
    #         weightColour = ColorChooserDialog()
    #         weightColour.show()
    #         weightColour = weightColour.result[2] #Retrieve hex
            
    #     elif button == "calories":
    #         caloriesColour = ColorChooserDialog()
    #         caloriesColour.show()
    #         caloriesColour = caloriesColour.result[2]

    #     elif button == "alpha":
    #         alphaColour = ColorChooserDialog()
    #         alphaColour.show()
    #         alphaColour = alphaColour.result[2]

    #     elif button == "targetweight":
    #         targetWeightColour = ColorChooserDialog()
    #         targetWeightColour.show()
    #         targetWeightColour = targetWeightColour.result[2]

    def saveSettings():
        if os.path.isfile("plotSettings.ini"):
            with open("plotSettings.ini", "w") as settingsFile:
                settingsEditor = configparser.ConfigParser()
                settings = {
                    "legendtoggle" : legendOptionsChoice1.get(),
                    "legendloc" : legendOptionsChoice2.get(),
                    "filltoggle" : chartOptionsChoice1.get(),
                    "fillalpha" : int(fillScale1.get()),
                    "charttitle" : chartTitleEntry1.get(),
                    "upperpadding" : upperPaddingButton1.get(),
                    "lowerpadding" : lowerPaddingButton1.get(),
                    "linewidth" : lineWidthSpinbox1.get(),
                    #"weightlinecolour" : weightColour,
                    #"calorieslinecolour" : caloriesColour,
                    #"alphalinecolour" :  alphaColour,
                    #"targetweightlinecolour" :  targetWeightColour,
                    }
                settingsEditor["Settings"] = settings
                settingsEditor.write(settingsFile)
                settingsWindow.destroy()

    settingsWindow = ttk.Toplevel(root)
    settingsWindow.resizable(True, True)
    settingsWindow.geometry("357x720")
    settingsWindow.title("Settings")
    settingsWindow.iconname(None)

    #Setting frames
    settingsFrame0 = ttk.LabelFrame(settingsWindow) #Umbrella frame
    settingsFrame1 = ttk.LabelFrame(settingsFrame0) #Relating to the title
    settingsFrame2 = ttk.LabelFrame(settingsFrame0) #Relating to the legend
    settingsFrame3 = ttk.LabelFrame(settingsFrame0) #Relating to the fill
    settingsFrame4 = ttk.LabelFrame(settingsFrame0) #Relating to the padding
    settingsFrame5 = ttk.LabelFrame(settingsFrame0) #Relating to lines
    settingsFrame10 = ttk.LabelFrame(settingsFrame0) #Relating to the padding. No.10 to leave space for further categories should they be added

    settingsFrame0.grid(row=0, column=0)
    settingsFrame1.grid(row=0, column=0)

    settingsFrame2.grid(row=1, column=0, sticky="ew")
    settingsFrame2.grid_rowconfigure(0, weight=1)
    settingsFrame2.grid_columnconfigure(0, weight=1)

    settingsFrame3.grid(row=2, column=0)
    settingsFrame4.grid(row=3, column=0)
    settingsFrame5.grid(row=4, column=0)
    settingsFrame10.grid(row=5, column=0)


    #Widgets

    chartTitleLabel1 = ttk.Label(settingsFrame1, font="helvetica, 12", text="Input chart title:")
    chartTitleEntry1 = ttk.Entry(settingsFrame1, font="helvetica, 12", justify="center")
    
    legendLabel1 = ttk.Label(settingsFrame2, text="Legend: ")
    legendLabel2 = ttk.Label(settingsFrame2, text="Choose location: ")

    legendOptionsList1 = ["enabled", "disabled"]
    legendOptionsList2 = ["upper left", 
                          "lower left", "upper right",
                          "upper left", "right",
                          "center left", "center right",
                          "center", "upper center"]
    
    legendOptionsChoice2 = tk.StringVar(root)
    legendOptionsChoice1 = tk.StringVar(root)

    legendButton1 = tk.OptionMenu(settingsFrame2, legendOptionsChoice1, *legendOptionsList1)
    legendButton2 = tk.OptionMenu(settingsFrame2, legendOptionsChoice2, *legendOptionsList2)

    chartFillLabel1 = ttk.Label(settingsFrame3, text="Enable or disable the fill between target and current:")
    chartOptionsList1 = ["enabled", "disabled"]
    chartOptionsChoice1 = tk.StringVar(root)
    chartFillOption1 = tk.OptionMenu(settingsFrame3, chartOptionsChoice1, *chartOptionsList1)
    fillScaleLabel1 = ttk.Label(settingsFrame3, text="Modify the opacity: ")
    fillScale1 = ttk.Scale(settingsFrame3, length=200, from_=0, to=100, command=slider)
    fillScaleLabel2 = ttk.Label(settingsFrame3, text="")

    paddingLabel1 = ttk.Label(settingsFrame4, text="Change upper padding: ")
    paddingLabel2 = ttk.Label(settingsFrame4, text="Change lower padding: ")
    upperPaddingButton1 = ttk.Spinbox(settingsFrame4, from_=3, to=100)
    lowerPaddingButton1 = ttk.Spinbox(settingsFrame4, from_=3, to=100)

    lineWidthLabel1 = ttk.Label(settingsFrame5, text="Change the width of lines: ")
    lineWidthSpinbox1 = ttk.Spinbox(settingsFrame5, from_=1, to=25)

    saveSettingsButton1 = ttk.Button(settingsFrame10, text="Save settings and close", command=lambda:saveSettings())

    if os.path.isfile("plotSettings.ini"):
        settingsReader = configparser.ConfigParser()
        settingsReader.read("plotSettings.ini")

        legendOptionsChoice1.set(settingsReader["Settings"]["legendtoggle"])
        legendOptionsChoice2.set(settingsReader["Settings"]["legendloc"])

        chartTitleEntry1.insert(0, settingsReader["Settings"]["charttitle"])

        chartOptionsChoice1.set(settingsReader["Settings"]["filltoggle"])
        fillAlphaLabelGet = settingsReader.getfloat(section="Settings", option="fillalpha")
        fillAlphaLabelReformed = int(fillAlphaLabelGet)
        fillScale1.set(fillAlphaLabelReformed)
        fillScaleLabel2.config(text=f"Current opacity: {fillAlphaLabelReformed}%")

        upperPaddingButton1.set(settingsReader["Settings"]["upperpadding"])
        lowerPaddingButton1.set(settingsReader["Settings"]["lowerpadding"])

        lineWidthSpinbox1.set(settingsReader["Settings"]["linewidth"])

    #weightLineColourButton = ttk.Button(settingsFrame5, text="Colour picker", command=lambda: colourChooser("weight"))
    #caloriesLineColourButton = ttk.Button(settingsFrame5, text="Colour picker", command=lambda: colourChooser("calories"))
    #alphaLineColourButton = ttk.Button(settingsFrame5, text="Colour picker", command=lambda: colourChooser("alpha"))
    #targetWeightLineColourButton = ttk.Button(settingsFrame5, text="Colour picker", command=lambda: colourChooser("targetweight"))

    #Grid
    
    legendLabel1.grid(row=0, column=0)
    legendButton1.grid(row=1, column=0)
    legendLabel2.grid(row=2, column=0,pady=5)
    legendButton2.grid(row=3, column=0)

    chartTitleLabel1.grid(row=3, column=0)
    chartTitleEntry1.grid(row=4, column=0)

    chartFillLabel1.grid(row=1, column=0)
    chartFillOption1.grid(row=2, column=0,pady=8)
    fillScaleLabel1.grid(row=3, column=0)
    fillScale1.grid(row=4, column=0)
    fillScaleLabel2.grid(row=5, column=0)

    paddingLabel1.grid(row=1, column=0)
    paddingLabel2.grid(row=3, column=0)
    upperPaddingButton1.grid(row=2, column=0)
    lowerPaddingButton1.grid(row=4, column=0)

    lineWidthLabel1.grid(row=0, column=0)
    lineWidthSpinbox1.grid(row=1, column=0)

    #weightLineColourButton.grid(row=2, column=0)
    #caloriesLineColourButton.grid(row=3, column=0)
    #alphaLineColourButton.grid(row=4, column=0)
    #targetWeightLineColourButton.grid(row=5, column=0)
    
    saveSettingsButton1.grid(row=0, column=0, pady=10)

#statistics
def openStatistics():
    statisticsWindow = ttk.Toplevel(root)
    statisticsWindow.resizable(True, True)
    statisticsWindow.geometry("325x175")
    statisticsWindow.title("Statistics")
    statisticsWindow.iconname(None)

    statisticsFrame0 = ttk.LabelFrame(statisticsWindow) #Umbrella frame
    statisticsFrame1 = ttk.LabelFrame(statisticsFrame0) #Statistics

    statisticsFrame0.grid(row=0, column=0)
    statisticsFrame1.grid(row=1, column=0)

    if os.path.isfile("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        measurement = config["Configuration"]["measurement"]

    data=pd.read_csv("inputdata.csv")
    peakWeightStatistic = data["weight"].max()
    peakWeightDateIndex = data["weight"].idxmax()
    peakWeightDateStatistic = data.loc[peakWeightDateIndex, "date"]

    peakCaloriesStatistic = data["calories"].max()
    peakCaloriesDateIndex = data["calories"].idxmax()
    peakCaloriesDateStatistic = data.loc[peakCaloriesDateIndex, "date"]

    averageWeightRoundedStatistic = data["weight"].mean().round(1) #Round the mean to 1 decimal place, removing .round() will give a mean with multiple numbers after decimal point
    averageCaloriesStatistic = data["calories"].mean().round(1) #as above, so below
    
    statisticsLabel0 = ttk.Label(statisticsFrame0, text="Statistics")
    statisticsLabel1 = ttk.Label(statisticsFrame1, text=f"Peak weight: {peakWeightStatistic} {measurement} on {peakWeightDateStatistic}")
    statisticsLabel2 = ttk.Label(statisticsFrame1, text=f"Highest daily calories: {peakCaloriesStatistic} kcal on {peakCaloriesDateStatistic}")
    statisticsLabel3 = ttk.Label(statisticsFrame1, text=f"Mean of calories: {averageCaloriesStatistic} kcal")
    statisticsLabel4 = ttk.Label(statisticsFrame1, text=f"Mean of weight: {averageWeightRoundedStatistic} {measurement}")
    #statisticsLabel5 = ttk.Label(statisticsFrame1, text=f"Rate of growth: {weightPercentChange}%")

    statisticsLabel0.grid(row=0, column=0)
    statisticsLabel1.grid(row=0, column=0)
    statisticsLabel2.grid(row=1, column=0)
    statisticsLabel3.grid(row=2, column=0)
    statisticsLabel4.grid(row=3, column=0)
    #statisticsLabel5.grid(row=4, column=0)
    
def openInformation():

    informationWindow = ttk.Toplevel(root)
    informationWindow.resizable(True, True)
    informationWindow.geometry("620x440")
    informationWindow.title("Entries")
    informationWindow.iconname(None)

    informationFrame1 = ttk.LabelFrame(informationWindow)
    informationFrame2 = ttk.LabelFrame(informationWindow)

    informationTree = ttk.Treeview(informationFrame1, columns=("date", "weight", "calories"), show="headings", height=20)
    informationTree.heading("date", text="Date")
    informationTree.heading("weight", text="Weight")
    informationTree.heading("calories", text="Calories")

    informationScroll = ttk.Scrollbar(informationWindow, orient=tk.VERTICAL, command=informationTree.yview)
    informationTree.configure(yscrollcommand=informationScroll.set)

    with open("inputdata.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            informationTree.insert("", tk.END, values=row)

    def editEntryWeight(): #Lacking CSV write
        selected = informationTree.selection()
        if selected:
            item = informationTree.item(selected)
            modification = simpledialog.askstring("Edit entry", "Modify weight:", initialvalue=item["values"][1])
            if modification is not None:
                informationTree.item(selected, values=(item['values'][0], modification, item['values'][2]))
    
    def editEntryCalories(): #Lacking CSV write
        selected = informationTree.selection()
        if selected:
            item = informationTree.item(selected)
            modification = simpledialog.askstring("Edit entry", "Modify calories:", initialvalue=item["values"][2])
            if modification is not None:
                informationTree.item(selected, values=(item['values'][0],item['values'][1], modification))


    def deleteEntry(): #Lacking CSV write
        selected = informationTree.selection()
        if selected:
            if messagebox.askyesno(title="Confirm deletion", message="Are you sure you want to delete this entry?"):
                informationTree.delete(selected)
            else:
                if selected:
                    messagebox.showinfo(title="Cancelled", message="Entry not removed")

    deleteEntryButton = ttk.Button(informationFrame2, text="Delete selected entry", command=lambda:deleteEntry())
    editCaloriesButton = ttk.Button(informationFrame2, text="Edit selected calories", command=lambda:editEntryCalories())
    editWeightButton = ttk.Button(informationFrame2, text="Edit selected weight", command=lambda:editEntryWeight())


    informationFrame1.grid(row=0, column=0)
    informationFrame2.grid(row=1, column=0)
    informationTree.grid(row=0, column=0, sticky="nsew")
    informationScroll.grid(row=0, column=1, sticky="ns")
    deleteEntryButton.grid(row=1, column=0)
    editWeightButton.grid(row=1, column=1)
    editCaloriesButton.grid(row=1, column=2)





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
    inputtedDate = cal.entry.get()
    inputtedCurrentWeight = weightCurrentInput.get()
    inputtedDailyCalories = dailyCaloriesEntry.get()

    columnsExist = os.path.isfile("inputdata.csv")
    
    with open("inputdata.csv", "a", newline="") as csvfile:
        columns = ["date", "weight", "calories"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        if not columnsExist:
            writer.writeheader()
        writer.writerow({"date": inputtedDate, "weight": inputtedCurrentWeight, "calories" : inputtedDailyCalories})
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
    weightDesiredInput.delete(0, tk.END)
    weightCurrentInput.delete(0, tk.END)
    dailyCaloriesEntry.delete(0, tk.END)

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
                if len(row) == 3:
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

def removeLastEntryConfirmation(csv_file): #Foresee editing this such that the user can pick a specific entry to delete
    RemoveLastEntryMsgBoxConfirmation = messagebox.askyesno(title="Are you sure?", message="Are you sure you wish to remove the most recent entry? This cannot be reversed")
    if RemoveLastEntryMsgBoxConfirmation == True:
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            contents = list(reader)
            contents.pop()
            with open(csv_file, 'w', newline='') as editFile:
                writer = csv.writer(editFile)
                writer.writerows(contents)
                messagebox.showinfo(title="Entry removed", message="Last entry was successfully removed")
    else:
        messagebox.showinfo(title="Cancelled", message="User cancelled: entry was not removed")

def generatePlot():
    #plt.xkcd()
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
        fillAlpha = int(settingsReader["Settings"]["fillalpha"])
        lineWidth = int(settingsReader["Settings"]["linewidth"])
        #weightLineColour = settingsReader["Settings"]["weightlinecolour"]
        #calouriesLineColour = settingsReader["Settings"]["calorieslinecolour"]
        #alphaLineColour = settingsReader["Settings"]["alphalinecolour"]
        #targetWeightLineColour = settingsReader["Settings"]["targetweightlinecolour"]
 
    else:
        pass
    if os.path.isfile("inputdata.csv"):
        data = pd.read_csv("inputdata.csv", parse_dates=["date"])
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        data.sort_index(inplace=True)
        data_resampled = data.resample("D", closed="left").mean()
        date = data_resampled.index
        weight_resampled = data_resampled["weight"]
        calories_resampled = data_resampled["calories"]
        
    else:
        pass

    plt.style.use("fivethirtyeight")

    fig, ax1 = plt.subplots()
    tick_spacing = 1
    ax1.plot(date, weight_resampled, label=f"Weight ({measurement})", color="blue", linewidth=float(lineWidth), linestyle="dashdot")
    ax1.tick_params(axis='y')
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.axhline(y=desiredWeight, linewidth=float(lineWidth), color="black", label="Target weight")

    ax2 = ax1.twinx()
    ax2.plot(date, calories_resampled, color="green", linewidth=float(lineWidth), label='Calories')
    ax2.set_ylabel('Calories')
    ax2.tick_params(axis='y')

    ax1.set_ylim(min(weight_resampled) - lowerYPadding, max(weight_resampled) + upperYPadding)
    #calories_ticks = range(0, int(max(calories_resampled)) + 250, 250)
    #ax2.set_yticks(calories_ticks)
    ax2.set_ylim(min(calories_resampled) - lowerYPadding*5, max(calories_resampled) + upperYPadding*5)
    if legendToggle == "enabled":
        fig.legend(handlelength=3,loc=legendLoc)
    ax1.set_xlabel("Date")
    ax1.set_ylabel(f"Weight in {measurement}")
    ax1.set_title(chartTitle)
    fig.subplots_adjust(left=0.1, bottom=0.1)
    if fillToggle == "enabled":
        ax1.fill_between(date, weight_resampled, desiredWeight, where=(weight_resampled <= desiredWeight), 
                         interpolate=True, color="blue", alpha=float(fillAlpha)/100, label="below weight target")
    plt.tight_layout()

    return plt

def showPlot():
    plot = generatePlot()
    plot.show()

def savePlotAsFile(plotGenerated): #This works but outputs, at the moment, a plot with dates clumped together
    generatePlot()
    chosenFilePath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if chosenFilePath:
        with open(chosenFilePath, "w") as f:
            plotGenerated.savefig(chosenFilePath)
            messagebox.showinfo(title="saved", message=f"Plot saved as image at {chosenFilePath} ")

    
#frames and widgets
Frame1 = ttk.LabelFrame(root)
Frame2 = ttk.LabelFrame(root)

cal = ttk.DateEntry(Frame1, bootstyle="info", startdate=datetime.now(), firstweekday=0)

l1 = ttk.Label(Frame1, font="helvetica, 12", text="Select the date: ")

l2 = ttk.Label(Frame1, font="helvetica, 12", text="Select weight measurement: ")
weightoption_list = ["kg", "lbs"]
weightMeasurementInputted = tk.StringVar(root)
weightMeasurementInputted.set("Select a measurement")
weightMeasurementOption = tk.OptionMenu(Frame1, weightMeasurementInputted, *weightoption_list)

l3 = ttk.Label(Frame1, font="helvetica, 12", text="Input target weight: ")
weightDesiredInput = ttk.Entry(Frame1, font="helvetica, 12")

l4 = ttk.Label(Frame1, font="Helvetica, 12", text="Input weight: ")
l5 = ttk.Label(Frame1, font="Helvetica, 12", text="Input daily calories: ")
weightCurrentInput = ttk.Entry(Frame1, font="helvetica, 12")
dailyCaloriesEntry = ttk.Entry(Frame1, font="helvetica, 12")

#Buttons
saveButton = ttk.Button(Frame1, text="Save entry", command=lambda: saveData())
removeLastEntryButton = ttk.Button(Frame2, text="Remove last entry", command=lambda: removeLastEntryConfirmation("inputdata.csv"))
loadButton = ttk.Button(Frame2, text="Load settings", command=lambda: loadData())
viewVisualization = ttk.Button(Frame2, text="View visualization", command=lambda: showPlot())
openSettingsButton = ttk.Button(Frame2, text="Edit plotting behaviour", command=lambda: openSettings())
savePlotButton = ttk.Button(Frame2, text="Save plot as image", command=lambda: savePlotAsFile(plotGenerated=generatePlot()))
openStatisticsButton = ttk.Button(Frame2, text="Open statistics", command=lambda: openStatistics())
openInformationButton = ttk.Button(Frame2, text="View all entries", command=lambda: openInformation())

Frame1.grid(row=0, column=0)
Frame2.grid(row=1, column=0)
l1.grid(row=0, column=0)
cal.grid(row=1, column=0)

l2.grid(row=2, column=0)
weightMeasurementOption.grid(row=3, column=0)

l3.grid(row=4, column=0)
weightDesiredInput.grid(row=5, column=0)

l4.grid(row=6, column=0)
weightCurrentInput.grid(row=7, column=0)
l5.grid(row=8, column=0)
dailyCaloriesEntry.grid(row=9, column=0)
saveButton.grid(row=10, column=0, pady=8)

removeLastEntryButton.grid(row=0, column=1)
loadButton.grid(row=0, column=2)
viewVisualization.grid(row=0, column=3)
openSettingsButton.grid(row=0, column=4)
savePlotButton.grid(row=0, column=5)
openStatisticsButton.grid(row=0, column=6)
openInformationButton.grid(row=0, column=7)

if __name__== "__main__":
    root.mainloop()