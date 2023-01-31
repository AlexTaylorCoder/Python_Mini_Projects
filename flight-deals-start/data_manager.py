from dotenv import load_dotenv
from flight_search import FlightSearch
import os 
import requests
from datetime import datetime

ENDPOINT = "https://api.sheety.co/a3e86da06554d3c95d2a951fe66f4bcd/flightTrackerInfo/sheet1"
class DataManager:
    def get():
        response = requests.get(ENDPOINT)
        response.raise_for_status()
        return response.json()["sheet1"]
    def add_city(name):
        DataManager.add_iata()
        code = FlightSearch.get_city(name)["locations"][0]["code"]
        body = {
            "sheet1": {
                "city":name,
                "iataCode":code
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
        print(sheet)
        for i,item in enumerate(sheet):
            if not item["iataCode"]:
                if "city" in item:
                    code = FlightSearch.get_city(item["city"])["locations"][0]["code"]
                    DataManager.patch_code(i,code)
                else:
                    DataManager.delete(i)
    def post(self,content):
        pass

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