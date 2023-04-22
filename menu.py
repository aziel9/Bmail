import tkinter
from tkinter import ttk
from tkinter import messagebox
import os
import openpyxl
from datetime import datetime


window = tkinter.Tk()
window.title("Truck Log Entry Form")

frame = tkinter.Frame(window)
frame.pack()

#saving truck logs
truck_info_frame = tkinter.LabelFrame(frame, text="Truck Information")
truck_info_frame.grid(row= 0, column=0, padx=20, pady=10)

release_number_label = tkinter.Label(truck_info_frame, text="Release Number")
release_number_label.grid(row=0,column=0)
truck_name_label = tkinter.Label(truck_info_frame, text="Truck Name")
truck_name_label.grid(row=0, column=1)
tare_info_label = tkinter.Label(truck_info_frame, text="Tare Weight")
tare_info_label.grid(row=0, column=2)
date_info_label = tkinter.Label(truck_info_frame, text="Date/Time")
date_info_label.grid(row=0, column=3)
gross_info_label = tkinter.Label(truck_info_frame, text = "Gross Weight")
gross_info_label.grid(row=0, column=4)


date_info_result_str = tkinter.StringVar()

release_number_entry = tkinter.Entry(truck_info_frame, textvariable=date_info_result_str)
truck_name_entry = tkinter.Entry(truck_info_frame)
tare_info_entry = tkinter.Entry(truck_info_frame)
#date_info_result = tkinter.Label(truck_info_frame, text='')
date_info_result = tkinter.Label(truck_info_frame)
date_info_result.grid(row=1, column=3)
date_info_result_str.trace('w', lambda *args: auto_date(release_number_entry.get()) )
release_number_entry.grid(row=1, column=0)
truck_name_entry.grid(row=1, column=1)
tare_info_entry.grid(row=1, column=2)


for widget in truck_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

def auto_date(release_filled):

    print("in auto_date function " + release_filled)
    #release_filled = release_number_entry.get()

    if len(release_filled) >= 6:
        print("in len area")
        #datetime object containing current date and time
        now = datetime.now()

        #format date and time to dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt_string
    else:
        print("made in error")
        #tkinter.messagebox.showwarning(title="Error", message="Please check release number")

window.mainloop()