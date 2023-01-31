#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime 

#Read she

#Take user input as city and find best deals
# sheet = DataManager()

# sheet.post()
# print(sheet)
# def add_city():
#     city = input("Add a city to the database.").strip()
#     code = FlightSearch.get_city(city)["locations"][0]["code"]
#     DataManager.add_city(city,code)

def add_city(dest,dateFrom=None, dateTo=None, price=None):
    #Add city with lowest price
    flightData = FlightSearch.search_flight_location(fly_from="New York", fly_to=dest)

    flights = []
    cheapest = flightData[0]
    DataManager.update_city_details(code=cheapest["cityCodeTo"], price=cheapest["price"],depart=format_date(cheapest["route"][0]["local_departure"]),arrive=format_date(cheapest["route"][-1]["local_arrival"]))

    for i,flight in enumerate(flightData):
        flightObj = {
            "airportFrom":flight["flyFrom"],
            "airportTo":flight["flyTo"],
            "nights":flight["nightsInDest"],
            "price":flight["price"],
            "availability":flight["availability"]["seats"],
            "airlines":flight["airlines"],
            "path":[route_data(route) for route in flight["route"]],
            "number":i
        }
        flights.append(flightObj)

def route_data(route):
    arrivalTime = format_date(route["local_arrival"])
    departureTime = format_date(route["local_departure"])
    airline = route["airline"]
    flightNo = route["flight_no"]
    flyFrom = route["flyFrom"]
    flyTo = route["flyTo"]
    bagRecheck = route["bags_recheck_required"]
    return arrivalTime,departureTime,airline,flightNo,flyFrom,flyTo,bagRecheck

def format_date(date):
    date = datetime.fromisoformat(date[:-1])
    return date.strftime('%m/%d/%y %H:%M')


def update_sheet_prices():
    DataManager.update_price_all()

def cheapest_flights():
    FlightSearch.search_cheapest_flights("NYC")

