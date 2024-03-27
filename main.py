import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox

root = tk.Tk()
root.geometry("400x400")
root.title("Weightplotter")
root.iconname(None)

def saveData():
    messagebox.showinfo("Saved", message="Date saved")
    pass


#frames
Frame1 = tk.LabelFrame(root)
Frame2 = tk.LabelFrame(root)

#Calendar function
currentDate = datetime.now()
currentDay = currentDate.day
currentMonth = currentDate.month
currentYear = currentDate.year

cal = Calendar(Frame1, selectmode = "day", 
               year = currentYear, 
               month = currentMonth, 
               day = currentDay)

inputtedDate = cal.get_date()

print()


#Frame1
l1 = ttk.Label(Frame1, font="helvetica, 12", text="Select the date: ")
CalendarSave = ttk.Button(Frame1, text="Save date", command=lambda: saveData())


#gridding/packing
cal.grid(row=0, column=1)
#Frame1
Frame1.grid(row=0, column=0)
l1.grid(row=0, column=0)
CalendarSave.grid(row=1, column=1)



root.mainloop()