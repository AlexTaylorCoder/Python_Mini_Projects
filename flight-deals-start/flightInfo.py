from customtkinter import *
from data_manager import DataManager
import requests
from bs4 import BeautifulSoup
BASE_ENDPOINT = "https://www.google.com/search"
class FlightInfo(CTkToplevel):
    def __init__(self,flightData):
        super().__init__()
        self.geometry(f"{600}x{600}")
        self.config(padx=50,pady=25)
        self.title("Flight Info")
        self.cityTo = flightData["cityTo"]
        self.price = flightData["price"]
        self.dateFrom = flightData["path"][0][1]
        self.dateTo = flightData["path"][-1][0]
        self.header = CTkFrame(master=self,bg_color="lightgrey",width=200,height=100)
        self.airline = flightData["airlines"][0]

        self.header.grid(row=0,column=3,columnspan=9,rowspan=3)


        datefromLabel = CTkLabel(master=self.header,text=self.dateFrom)
        datetoLabel = CTkLabel(master=self.header,text=self.dateTo)
        cityLabel = CTkLabel(master=self.header,text=self.cityTo)
        priceLabel = CTkLabel(master=self.header,text=f"${self.price}")
        self.save = CTkButton(master=self.header,text="Track",command=self.save_flight)

        datefromLabel.pack(side=LEFT,padx=5)
        datetoLabel.pack(side=LEFT,padx=5)
        cityLabel.pack(side=LEFT,padx=5)
        priceLabel.pack(side=LEFT,padx=5)
        self.save.pack(side=LEFT,padx=10)

        for i,route in enumerate(flightData["path"]):
            routeFrame = CTkFrame(master=self,width=200,height=100,bg_color="lightgrey")
            routeFrame.grid(column=2,row=i+3,columnspan=10,pady=10)
            for item in route:
                routeLabel = CTkLabel(master=routeFrame,text=item)
                routeLabel.pack(side=LEFT,padx=5)
    def save_flight(self):
        status = DataManager.post_from_gui_saved_flights(self.cityTo,self.dateFrom,self.dateTo,self.price)
        if status:
            self.save.configure(text="Saved!")
        else:
            self.save.configure(text="DB Error!")
    def find_source(self):
        params = {
            "q":f"{self.airline}+airlines+to+{self.cityTo}"
        }
        response = requests.get(f"BASE_ENDPOINT",params=params)
        

