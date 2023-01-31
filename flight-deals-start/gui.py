from customtkinter import *
import tkinter
from tkcalendar import Calendar, DateEntry
from main import add_city, route_data, update_sheet_prices

set_appearance_mode("System")
set_default_color_theme("blue")

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{750}x{600}")
        self.config(padx=50,pady=25)
        self.title("Flight Tracker")

        self.label = CTkLabel(master=self,text="Random")
        self.email_notif = CTkCheckBox(master=self)
        self.text_notif = CTkCheckBox(master=self)
        self.dateFrom = DateEntry(self,width= 16, background= "black", foreground= "white",bd=2,font="Arial 14", selectmode='day',cursor="hand1")
        self.dateFrom.delete(0,END)
        self.dateFrom.insert(0,"Departure Date")
        self.dateTo = DateEntry(self,width= 16, background= "black", foreground= "white",bd=2,font="Arial 14", selectmode='day',cursor="hand1")
        self.dateTo.delete(0,END)
        self.dateTo.insert(0,"Rearrival Date")
        self.city_input = CTkEntry(master=self,placeholder_text="City")
        self.price_input = CTkEntry(master=self,placeholder_text="Max $")
        self.searchButton = CTkButton(master=self,text="Search",width=200,height=50,command=self.read_inputs)
        self.refresh = CTkButton(master=self,text="\u27F3",width=20)
        # self.itemContainer = CTkFrame(master=self,width=630,height=420,corner_radius=10,border_color="darkgrey",border_width=3)
        self.tabView = CTkTabview(master=self,width=630,height=420,corner_radius=10,border_color="darkgrey",border_width=3)
        self.tabView.grid(column=1,row=7)

        self.recTab = self.tabView.add("Suggested")
        self.saveTab = self.tabView.add("Saved")
       # ... create widgets ...
    def read_inputs(self):
        city = self.city_input.get()
        add_city(dest=self.city_input.get(),dateFrom=self.dateFrom.get(),dateTo=self.dateTo.get(),price=self.price_input.get())
    def position(self):
        # self.label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        # self.city_input.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.tabView.grid(column=1,row=1,rowspan=8,columnspan=11,pady=10,padx=10)
        self.dateFrom.grid(column=1,row=9,columnspan=2)
        self.dateTo.grid(column=3,row=9, columnspan=2)
        self.city_input.grid(column=5,row=9,columnspan=2)
        self.price_input.grid(column=7,row=9,columnspan=1)
        self.searchButton.grid(column=3,row=10,columnspan=4,pady=20)
        self.refresh.grid(column=7,row=10,padx=5,pady=20)
    def add_flight_element(self,row):
        flightFrame = CTkFrame(master=self,width=570,height=70,corner_radius=10,border_width=1,border_color="black",fg_color="lightgray")

        datefromLabel = CTkLabel(master=self,text="Random text",bg_color="lightgrey")
        datetoLabel = CTkLabel(master=self,text="Random text",bg_color="lightgrey")
        cityLabel = CTkLabel(master=self,text="Random text",bg_color="lightgrey")
        priceLabel = CTkLabel(master=self,text="Random text",bg_color="lightgrey")



        flightFrame.grid(column=1,row=row,padx=5,pady=5,columnspan=8)
        datefromLabel.grid(column=1,row=row,padx=5,pady=5,columnspan=2)
        datetoLabel.grid(column=3,row=row,padx=5,pady=5,columnspan=2)
        cityLabel.grid(column=6,row=row,padx=5,pady=5)
        priceLabel.grid(column=7,row=row,padx=5,pady=5)


        # self.dateFrom.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
   # ... program methods ...


def startGUI():
    app = App()
    app.position()
    app.mainloop()

startGUI()
