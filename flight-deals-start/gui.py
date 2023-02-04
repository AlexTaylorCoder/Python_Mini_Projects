from customtkinter import *
from tkcalendar import DateEntry
from main import add_city, route_data, update_sheet_prices,load_cheapest
from data_manager import DataManager
from scrollableFrame import ScrollableFrame
from flightInfo import FlightInfo

set_appearance_mode("System")
set_default_color_theme("blue")

# class scrollTabView(CTkTabview):
#     def __init__(self):
#         super().__init__()
#         self.sFrame = ScrollableFrame(self)    


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{750}x{600}")
        self.config(padx=50,pady=25)
        self.title("Flight Tracker")

        self.label = CTkLabel(master=self,text="Random")
        self.email_notif = CTkCheckBox(master=self)
        self.text_notif = CTkCheckBox(master=self)
        self.dateFrom = DateEntry(self,background= "black", foreground= "white",bd=2,font="Arial 14", selectmode='day',cursor="hand1")
        self.dateFrom.delete(0,END)
        self.dateFrom.insert(0,"Departure Date")
        self.dateTo = DateEntry(self,background= "black", foreground= "white",bd=2,font="Arial 14", selectmode='day',cursor="hand1")
        self.dateTo.delete(0,END)
        self.dateTo.insert(0,"Rearrival Date")
        self.city_input = CTkEntry(master=self,placeholder_text="City")
        self.price_input = CTkEntry(master=self,placeholder_text="Max $",width=40)
        self.searchButton = CTkButton(master=self,text="Search",command=self.read_inputs)
        self.refresh = CTkButton(master=self,text="\u27F3",width=20)

        self.addCityInput = CTkEntry(master=self,placeholder_text="Remember City")
        self.addCityButton = CTkButton(master=self,text="Save",command=self.save_city)

        self.tabView = CTkTabview(master=self,width=630,height=420,corner_radius=10,border_color="darkgrey",border_width=3)

        self.recTab = self.tabView.add("Suggested")
        self.saveTab = self.tabView.add("Saved")

        print(self.recTab.winfo_width())
        print(self.tabView.winfo_width())

        self.sFrame = ScrollableFrame(self.recTab)    
        self.rFrame = ScrollableFrame(self.saveTab)

        self.tabView.pack()

        self.rFrame.pack(fill="both",expand=True)
        self.sFrame.pack(fill="both", expand=True)
        self.tabView.set("Suggested")

       # ... create widgets ...
    def read_inputs(self):
        add_city(dest=self.city_input.get(),dateFrom=self.dateFrom.get(),dateTo=self.dateTo.get(),price=self.price_input.get())
    def save_city(self):
        DataManager.add_city(self.addCityInput.get())

    def position(self):
        self.tabView.grid(column=1,row=1,rowspan=8,columnspan=11,pady=10)
        self.dateFrom.grid(column=2,row=9,columnspan=1)
        self.dateTo.grid(column=3,row=9, columnspan=1)
        self.city_input.grid(column=5,row=9,columnspan=3)
        self.price_input.grid(column=8,row=9,columnspan=1)
        self.searchButton.grid(column=9,row=9,columnspan=2,padx=10)
        self.refresh.grid(column=7,row=10,padx=5,pady=20)

        self.addCityInput.grid(column=3,row=10,columnspan=2,padx=10)
        self.addCityButton.grid(column=5,row=10,columnspan=2,padx=10)
    def add_flight_element_from_spreadsheet(self,row,sheetData):
        #Remove from flight sheet also
        flightFrame = CTkFrame(master=self.rFrame.scrollable_frame,width=600,height=400,corner_radius=10,border_width=1,border_color="black",fg_color="lightgray")

        row += 2

        datefromLabel = CTkLabel(master=flightFrame,text=sheetData["dateDeparture"],bg_color="lightgrey")
        datetoLabel = CTkLabel(master=flightFrame,text=sheetData["dateReturn"],bg_color="lightgrey")
        cityLabel = CTkLabel(master=flightFrame,text=sheetData["city"],bg_color="lightgrey")
        priceLabel = CTkLabel(master=flightFrame,text=f'${sheetData["lowestPrice"]}',bg_color="lightgrey")
        removeButton = CTkButton(master=flightFrame,text="Remove")

        flightFrame.pack(pady=5)
 
        datefromLabel.grid(column=2,row=row,padx=5,columnspan=2)
        datetoLabel.grid(column=4,row=row,padx=5,columnspan=2)
        cityLabel.grid(column=6,row=row,padx=5)
        priceLabel.grid(column=8,row=row,padx=5)
        removeButton.grid(column=9,columnspan=2)

        def remove_flight(event):
            pass

    def add_flight_element(self,row,flightData):
        flightFrame = CTkFrame(master=self.sFrame.scrollable_frame,width=600,height=400,corner_radius=10,border_width=1,border_color="black",fg_color="lightgray")
        airlineFrame = CTkFrame(master=flightFrame,width=50,height=50,corner_radius=5,border_width=1,border_color="darkgray",fg_color="lightgray")

        row += 2
        # if "airlines" in flightData:
        #     airline = CTkLabel(master=airlineFrame,text=flightData["airlines"][0],bg_color="lightgrey")
        #     airline.pack()
        # else:
        #     print(flightData)

        datefromLabel = CTkLabel(master=flightFrame,text=flightData["path"][0][1],bg_color="lightgrey")
        datetoLabel = CTkLabel(master=flightFrame,text=flightData["path"][-1][0],bg_color="lightgrey")
        cityLabel = CTkLabel(master=flightFrame,text=flightData["cityTo"],bg_color="lightgrey")
        priceLabel = CTkLabel(master=flightFrame,text=f'${flightData["price"]}',bg_color="lightgrey")

        flightFrame.pack(pady=5)
 
        airlineFrame.grid(column=2,row=row,padx=8,columnspan=2)
        datefromLabel.grid(column=4,row=row,padx=5,columnspan=2)
        datetoLabel.grid(column=6,row=row,padx=5,columnspan=2)
        cityLabel.grid(column=8,row=row,padx=5)
        priceLabel.grid(column=9,row=row,padx=5)

        def expand_flight(event):
            FlightInfo(flightData)

        flightFrame.bind("<Button-1>",expand_flight)
        # airlineFrame.bind("<Button-1>",expand_flight)



def startGUI():
    #Will need multithreading to fully optimize
    app = App()
    load_rec(app)
    load_saved(app)


    app.mainloop()

def load_rec(app):
    organizedFlightData = load_cheapest()
    for i,flight in enumerate(organizedFlightData):
        app.add_flight_element(i,flight)
def load_saved(app):
    saved = DataManager.get_saved()
    for row,item in enumerate(saved):
        app.add_flight_element_from_spreadsheet(row,item)
    

startGUI()
