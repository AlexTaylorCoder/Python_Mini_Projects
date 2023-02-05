from customtkinter import *
from data_manager import DataManager
import requests
import webbrowser
from bs4 import BeautifulSoup
FLIGHT_ELEMENT_FONT = ("Arial", 25)
BASE_ENDPOINT = "https://www.google.com/search"
class FlightInfo(CTkToplevel):
    def __init__(self,flightData):
        super().__init__()
        self.geometry(f"{700}x{600}")
        self.config(padx=50,pady=25)
        self.title("Flight Info")
        self.cityTo = flightData["cityTo"]
        self.price = flightData["price"]
        self.dateFrom = flightData["path"][0][1]
        self.dateTo = flightData["path"][-1][0]
        self.header = CTkFrame(master=self,bg_color="lightgrey",width=200,height=100)
        self.airline = flightData["airlines"][0]
        self.link = None

        self.header.grid(row=0,column=3,columnspan=9,rowspan=3)

            
        self.linkButton = CTkButton(master=self,text="Site",command=self.find_source,font=("Arial", 22))
        self.save = CTkButton(master=self,text="Track",command=self.save_flight,font=("Arial", 22))


        datefromLabel = CTkLabel(master=self.header,text=self.dateFrom,font=FLIGHT_ELEMENT_FONT)
        datetoLabel = CTkLabel(master=self.header,text=self.dateTo,font=FLIGHT_ELEMENT_FONT)
        cityLabel = CTkLabel(master=self.header,text=self.cityTo,font=FLIGHT_ELEMENT_FONT)
        priceLabel = CTkLabel(master=self.header,text=f"${self.price}",font=FLIGHT_ELEMENT_FONT)
    

        datefromLabel.pack(side=LEFT,padx=5,pady=5)
        datetoLabel.pack(side=LEFT,padx=5,pady=5)
        cityLabel.pack(side=LEFT,padx=5,pady=5)
        priceLabel.pack(side=LEFT,padx=5,pady=5)


        count = 0
        for route in flightData["path"]:
            routeFrame = CTkFrame(master=self,width=200,height=100,bg_color="lightgrey",border_width=1,border_color="darkgrey",corner_radius=5)
            routeFrame.grid(column=2,row=count+3,columnspan=10,pady=10)
            for item in route:
                print(item)
                # if type(item) == bool:

                routeLabel = CTkLabel(master=routeFrame,text=item,font=("Arial", 23))
                routeLabel.pack(side=LEFT,padx=5,pady=5)
            count += 1
        
        self.linkButton.grid(column=5,columnspan=2,row=count+3,rowspan=2,padx=8,pady=8)
        self.save.grid(column=7,columnspan=2,row=count+3,rowspan=2,padx=8,pady=8)
    def save_flight(self):
        if self.link:
            link = self.link
        else:
            link = self.find_link()
        status = DataManager.post_from_gui_saved_flights(self.cityTo,self.dateFrom,self.dateTo,self.price,link)
        if status:
            self.save.configure(text="Saved!")
            self.save.destroy()
        else:
            self.save.configure(text="DB Error!")
    def find_source(self):
        self.linkButton.configure(text="Loading...")
        #Need to fill in params
        params = {
            "q":f"{self.airline}+airlines+to+{self.cityTo}"
        }
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Accept-Language":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        response = requests.get(BASE_ENDPOINT,params=params,headers=headers)
        airline_data = response.text
        soup = BeautifulSoup(airline_data,"html.parser")
        top_link = soup.select_one(".g a")["href"]
        self.link = top_link
        webbrowser.open_new_tab(top_link)

        self.linkButton.configure(text="Site")
    def find_link(self):
        params = {
            "q":f"{self.airline}+airlines+to+{self.cityTo}"
        }
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Accept-Language":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        response = requests.get(BASE_ENDPOINT,params=params,headers=headers)
        airline_data = response.text
        soup = BeautifulSoup(airline_data,"html.parser")
        top_link = soup.select_one(".g a")["href"]
        return top_link

        

