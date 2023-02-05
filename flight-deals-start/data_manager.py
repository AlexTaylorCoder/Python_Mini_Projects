from dotenv import load_dotenv
from flight_search import FlightSearch
import os 
import requests
from datetime import datetime

ENDPOINT = "https://api.sheety.co/a3e86da06554d3c95d2a951fe66f4bcd/flightTrackerInfo/sheet1"
SAVEDENDPOINT = "https://api.sheety.co/a3e86da06554d3c95d2a951fe66f4bcd/flightTrackerSaved/sheet1/"
class DataManager:
    def get():
        response = requests.get(ENDPOINT)
        response.raise_for_status()
        return response.json()["sheet1"]
    def get_saved():
        response = requests.get(SAVEDENDPOINT)
        response.raise_for_status()
        return response.json()["sheet1"]
    def cityPresence(name):
        for row,item in enumerate(DataManager.get()):
            if item["city"] == name:
                return row
        return False
    def add_city(name):            
        code = FlightSearch.get_city_code(name)
        flightData = FlightSearch.search_flight_by_iata(code_from="NYC",code_to=code,limit=1)

        cheapest = flightData[0]
        price = cheapest["price"]
        dateDeparture = cheapest["route"][0]["local_departure"]
        dateReturn = cheapest["route"][-1]["local_arrival"]

        #Checks for duplicate city
        isDuplicate = DataManager.cityPresence(name)
        if isDuplicate:
            return DataManager.patch_content(row=isDuplicate,price=price,depart=dateDeparture,arrive=dateReturn)

        body = {
            "sheet1": {
                "city":name,
                "iataCode":code,
                "lowestPrice":price,
                "dateDeparture": format_date(dateDeparture),
                "dateReturn": format_date(dateReturn)

            }
        }
        response = requests.post(ENDPOINT,json=body)
        response.raise_for_status()
        return response.json()

    def update_city_details(code,price,depart,arrive):
        DataManager.add_iata()
        sheet = DataManager.get()
        for row,item in enumerate(sheet):
            if item["iataCode"] == code:
                DataManager.patch_content(row,price,depart,arrive)        

    def update_price_all():
        DataManager.add_iata()
        sheet = DataManager.get()
        for row,item in enumerate(sheet):
            #Need to check flights
            flightData = FlightSearch.search_flight_by_iata(code_from="NYC",code_to=item["iataCode"])
            if flightData:
                cheapest = flightData[0]
                DataManager.patch_content(row,cheapest["price"],depart=format_date(cheapest["route"][0]["local_departure"]),arrive=format_date(cheapest["route"][-1]["local_arrival"]))
    def add_iata():
        sheet = DataManager.get()
        for i,item in enumerate(sheet):
            if not item["iataCode"]:
                if "city" in item:
                    code = FlightSearch.get_city(item["city"])["locations"][0]["code"]
                    DataManager.patch_code(i,code)
                else:
                    DataManager.delete(i)
    def post_from_gui_saved_flights(cityTo,dateFrom,dateTo,price,link):
        body = {
            "sheet1": {
                "city":cityTo,
                "lowestPrice": price,
                "dateDeparture":dateFrom,
                "dateReturn":dateTo,
                "link":link
            }
        }
        response = requests.post(SAVEDENDPOINT,json=body)
        try:
            response.raise_for_status()
        except:
            return False
        else:
            return True
    def remove_saved_row(row):
        #first find row then delete
        response = requests.delete(f"{SAVEDENDPOINT}/{row}")

    def find_row_by(param,query,data):
        for i,item in enumerate(data):
            if item[param] == query:
                return i + 2
        return False

    def delete(row):
        response = requests.delete(f"{ENDPOINT}/{row+2}")
        return "Removed"
    def patch_code(row,code):
        body = {
             "sheet1": {
                "iataCode":code
            }
        }
        #Row corresponds to number of left, not index of array
        response = requests.put(f"{ENDPOINT}/{row+2}",json=body)
        return "patched"
    def patch_content(row,price,depart,arrive):
        body = {
            "sheet1": {
                "lowestPrice": price,
                "dateDeparture":depart,
                "dateReturn":arrive
            }
        }
        response = requests.put(f"{ENDPOINT}/{row+2}",json=body)
        response.raise_for_status()
        return response.json()

def format_date(date):
    date = datetime.fromisoformat(date[:-1])
    return date.strftime('%m/%d/%y %H:%M')