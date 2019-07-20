import tkinter
import webbrowser
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Script Version and Author
__version__ = '1.0'
__author__ = 'Michael Jeans'

# set up connection to SQLite3 db
db_file = "chair.db"
conn = sqlite3.connect(db_file)
c = conn.cursor()


def get_data(vsr):
    global lat
    global long
    parameter = choiceBox.get()
    c.execute("SELECT Clinic_ID, Clinic_Name, Clinic_State, Clinic_Subnet, TZone, OG, Helmer, Clinic_LAT, Clinic_LONG "
              " FROM Clinic WHERE Clinic_ID = {}".format(parameter))
    data = c.fetchall()
    c.execute("SELECT Printer_Man, Printer_Model, Printer_IP "
              " FROM Clinic_Printers  WHERE Clinic_ID = {} AND Printer_Man = 'Lexmark' "
              " AND SUBSTR(Printer_Model,1,2) = 'MX' ORDER BY Printer_IP LIMIT 1".format(parameter))
    printers = c.fetchall()

    choiceBox.set('')
    clinicID.set(data[0][0])
    clinicName.set(data[0][1])
    clinicState.set(data[0][2])
    clinicSubnet.set(data[0][3] + '.1')
    try:
        tz = data[0][4][8:]
    except TypeError:
        tz = "No timezone info"
    except IndexError:
        pass
    if tz == "Puerto_Rico":
        timezone = "Georgetown, La Paz, Manaus, San Juan"
    elif tz == "New_York":
        timezone = "Eastern Time"
    elif tz == "Detroit":
        timezone = "Eastern Time"
    elif tz == "Indiana/Indianapolis":
        timezone = "Indiana (East)"
    elif tz == "Chicago":
        timezone = "Central Time"
    elif tz == "Denver":
        timezone = "Mountain Time"
    elif tz == "Phoenix":
        timezone = "Arizona"
    elif tz == "Los_Angeles":
        timezone = "Pacific Time"
    elif tz == "Anchorage":
        timezone = "Alaska"
    elif tz == "Honolulu":
        timezone = "Hawaii"
    else:
        timezone = tz
    clinicTimeZone.set(timezone)
    if data[0][5] == "PPS":
        og = "PPMS"
    else:
        og = data[0][5]
    clinicOG.set(og)
    try:
        helmer = data[0][6].strip()
    except AttributeError:
        helmer = "None"
    helmer = helmer.replace("s:", "green .")
    helmer = helmer.replace('h:', 'blue .')
    helmer = helmer.replace(',', ', ')
    clinicHelmer.set(helmer)

    # Add logic to get value of helmer and set background accordingly.
    both = ['green', 'blue']
    if all(x in helmer for x in both):
        clinicHelmerResult.configure(background='#99ffcc', foreground='#000000')
    elif 'green' in helmer:
        clinicHelmerResult.configure(background='#00ff00', foreground='#000000')
    elif 'blue' in helmer:
        clinicHelmerResult.configure(background='#0099ff', foreground='#000000')
    else:
        clinicHelmerResult.configure(background='#000000', foreground='#ffffff')
    lat = data[0][7]
    long = data[0][8]
    try:
        clinicPrinter.set(printers[0][0] + " " + printers[0][1])
        clinicPrinterIP.set(data[0][3] + "." + printers[0][2].strip())
    except IndexError:
        clinicPrinter.set("N/A")
        clinicPrinterIP.set("N/A")

    return data


def clinic_list():
    c.execute("SELECT Clinic_ID FROM Clinic ORDER BY Clinic_ID")
    data = c.fetchall()
    cliniclist = []
    for row in data:
        if len(str(row[0])) >= 4:
            cliniclist.append(row[0])
    return cliniclist


def webmap():
    if lat is not None and long is not None:
        webbrowser.open("https://www.google.com/maps/?q=" + lat + "," + long + "&ll=" + lat + "," + long +
                        "&z=18", new=1)
    else:
        messagebox.showinfo("Google Map", "No location info available")


# Tkinter window properties
mainWindow = tkinter.Tk()

clinicChoice = tkinter.Variable(mainWindow)
clinicID = tkinter.Variable(mainWindow)
clinicName = tkinter.Variable(mainWindow)
clinicState = tkinter.Variable(mainWindow)
clinicSubnet = tkinter.Variable(mainWindow)
clinicTimeZone = tkinter.Variable(mainWindow)
clinicOG = tkinter.Variable(mainWindow)
clinicHelmer = tkinter.Variable(mainWindow)
clinicPrinter = tkinter.Variable(mainWindow)
clinicPrinterIP = tkinter.Variable(mainWindow)

mainWindow.title("Rounding Laptop Lookup Tool")
window_width = mainWindow.winfo_reqwidth()
window_height = mainWindow.winfo_reqheight()
mainWindow.resizable(False, False)
mainWindow.focusmodel('active')
position_right = int(mainWindow.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(mainWindow.winfo_screenheight() / 3 - window_height / 3)
mainWindow.geometry("+{}+{}".format(position_right, position_down))
mainWindow['padx'] = 40
mainWindow['pady'] = 10

# Row 0
choiceLabel = tkinter.Label(mainWindow, text="Select clinic:")
choiceLabel.grid(row=0, column=0)
choiceBox = ttk.Combobox(mainWindow, width=5, values=clinic_list(), takefocus=1)
choiceBox.grid(row=0, column=1, columnspan=2, sticky='ew')

# Row 1
clinicIDLabel = tkinter.Label(mainWindow, text="Clinic ID")
clinicIDLabel.grid(row=1, column=0)
clinicNameLabel = tkinter.Label(mainWindow, text="Clinic Name")
clinicNameLabel.grid(row=1, column=1)
clinicStateLabel = tkinter.Label(mainWindow, text="Clinic State")
clinicStateLabel.grid(row=1, column=2)

# Row 2
clinicIDResult = tkinter.Label(mainWindow, relief="solid", textvariable=clinicID)
clinicIDResult.grid(row=2, column=0, sticky='ew')
clinicNameResult = tkinter.Label(mainWindow, relief="solid", padx='5', textvariable=clinicName)
clinicNameResult.grid(row=2, column=1, sticky='ew')
clinicStateResult = tkinter.Label(mainWindow, relief="solid", textvariable=clinicState)
clinicStateResult.grid(row=2, column=2, sticky='ew')

# Row 3
clinicSubnetLabel = tkinter.Label(mainWindow, text="Clinic Subnet")
clinicSubnetLabel.grid(row=3, column=0)
clinicTimeZoneLabel = tkinter.Label(mainWindow, text="Clinic Time Zone")
clinicTimeZoneLabel.grid(row=3, column=1)
clinicOGLabel = tkinter.Label(mainWindow, text="Clinic OG")
clinicOGLabel.grid(row=3, column=2)

# Row 4
clinicSubnetResult = tkinter.Label(mainWindow, relief="solid", textvariable=clinicSubnet)
clinicSubnetResult.grid(row=4, column=0, sticky='ew')
clinicTimeZoneResult = tkinter.Label(mainWindow, relief="solid", padx='5', textvariable=clinicTimeZone)
clinicTimeZoneResult.grid(row=4, column=1, sticky='ew')
clinicOGResult = tkinter.Label(mainWindow, relief="solid", textvariable=clinicOG)
clinicOGResult.grid(row=4, column=2, sticky='ew')

# Row 5
clinicHelmerLabel = tkinter.Label(mainWindow, text="Clinic Helmer")
clinicHelmerLabel.grid(row=5, column=0)
clinicPrinterLabel = tkinter.Label(mainWindow, text="Default Printer")
clinicPrinterLabel.grid(row=5, column=1)
clinicPrinterIPLabel = tkinter.Label(mainWindow, text="Printer IP")
clinicPrinterIPLabel.grid(row=5, column=2)

# Row 6
clinicHelmerResult = tkinter.Label(mainWindow, relief="solid", padx='5', textvariable=clinicHelmer)
clinicHelmerResult.grid(row=6, column=0, sticky='ew')
clinicPrinterResult = tkinter.Label(mainWindow, relief="solid", textvariable=clinicPrinter)
clinicPrinterResult.grid(row=6, column=1, sticky='ew')
clinicPrinterIPResult = tkinter.Label(mainWindow, relief="solid", padx='5', textvariable=clinicPrinterIP)
clinicPrinterIPResult.grid(row=6, column=2, sticky='ew')

# Row 7
GoogleMapLabel = tkinter.Label(mainWindow, text="Google Map")
GoogleMapLabel.grid(row=7, column=1)

# Row 8
GoogleMapButton = tkinter.Button(mainWindow, text="Clinic Area Map", command=webmap)
GoogleMapButton.grid(row=8, column=1, sticky='ew')

choiceBox.focus()
choiceBox.bind("<<ComboboxSelected>>", get_data)
choiceBox.bind("<Return>", get_data)

mainWindow.mainloop()
