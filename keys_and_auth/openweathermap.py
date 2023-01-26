import requests
import datetime as dt
from twilio.rest import Client
import os

ACCOUNT_SID = "AC46488998e7476f389f1cb0eecbe75e23"
AUTH = os.environ.get("AUTH_TOKEN")

params = {
    "lat": 40.734859, 
    "lon": -73.985563,
    "appid": os.environ.get("OWN_APPID"),
    "exclude":"current,minutely,daily"
}
def check_weather():
    hour = dt.datetime.now().hour
    response = requests.get("http://api.openweathermap.org/data/2.5/onecall",params=params)
    response.raise_for_status()
    weather_data = response.json()

    for hour in range(hour, hour+12):
        if int(weather_data["hourly"][hour]["weather"][0]["id"]) < 700:
            return True 
    return False 

def main():
    if check_weather():
        client = Client(ACCOUNT_SID,AUTH)
        message = client.messages.create(
            body="It's going to rain today. Bring an umbrella!",
            from_ = "+19405319275",
            to = "+19178064701"
        )
        print(message.status)

main()