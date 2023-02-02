from dotenv import load_dotenv
import os 
import requests
import datetime as dt
from dotenv import load_dotenv

load_dotenv()
SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
LOCATION_DUMP_ENDPOINT = "https://api.tequila.kiwi.com/locations/dump"
LOCATION_QUERY_ENPOINT = "https://api.tequila.kiwi.com/locations/query"

KEY = os.getenv("TEQUILA_PASSWORD")
headers = {
    "apikey":KEY
}

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_cities():
        body = {
            "location_types":"city",
        }
        response = requests.get(LOCATION_DUMP_ENDPOINT,headers=headers,json=body)
        response.raise_for_status()
        return response.json()

    def get_city(city):
        params = {
            "term":city,
            "location_types":"city",
        }
        response = requests.get(LOCATION_QUERY_ENPOINT,headers=headers,params=params)
        response.raise_for_status()
        return response.json()
    def get_city_code(city):
        return FlightSearch.get_city(city)["locations"][0]["code"]

    def search_cheapest_flights(fly_from,date_from=dt.datetime.now() + dt.timedelta(days=60),date_to=dt.datetime.now() + dt.timedelta(days=80), price=600):
        
        #Find cheapest
        date_from =date_from.strftime("%d/%m/%Y")
        date_to = date_to.strftime("%d/%m/%Y")
        params = {
            "fly_from":f"city:{fly_from}",
            "dateFrom":date_from,
            "dateTo":date_to,
            "nights_in_dst_from":10,
            "nights_in_dst_to":30,
            "price_to":price,
            "flight_type":"round",
            "limit":10
        }

        response = requests.get(SEARCH_ENDPOINT,headers=headers,params=params)
        return response.json()["data"]

    def search_flight_location(fly_from,fly_to,date_from=dt.datetime.now() + dt.timedelta(days=60),date_to=dt.datetime.now() + dt.timedelta(days=80)):
        #Fly from must be code
        code_from = FlightSearch.get_city_code(fly_from)
        code_to = FlightSearch.get_city_code(fly_to)

        return FlightSearch.search_flight(code_from=code_from,code_to=code_to,date_from=date_from,date_to=date_to)


    def search_flight(code_from,code_to,date_from=dt.datetime.now() + dt.timedelta(days=60),date_to=dt.datetime.now() + dt.timedelta(days=80),limit=5):
        if code_from == code_to:
            return False
        date_from =date_from.strftime("%d/%m/%Y")
        date_to = date_to.strftime("%d/%m/%Y")
        params = {
            "fly_from":f"city:{code_from}",
            "fly_to":f"city:{code_to}",
            "dateFrom":date_from,
            "dateTo":date_to,
            "nights_in_dst_from":10,
            "nights_in_dst_to":30,
            "price_to":2000,
            "flight_type":"round",
            "limit":limit
        }

        response = requests.get(SEARCH_ENDPOINT,headers=headers,params=params)
        return response.json()["data"]

    def search_flight_by_iata(code_from,code_to,date_from=dt.datetime.now() + dt.timedelta(days=60),date_to=dt.datetime.now() + dt.timedelta(days=80),limit=None):
        return FlightSearch.search_flight(code_from,code_to,date_from,date_to,limit)


