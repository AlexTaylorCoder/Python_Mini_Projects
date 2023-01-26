import requests
from dotenv import load_dotenv
import os
import datetime as dt

load_dotenv()

NUTRITION_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
GET_SHEETS_ENDPOINT = "https://api.sheety.co/a3e86da06554d3c95d2a951fe66f4bcd/myWorkouts/workouts"
ADD_ROW_SHEETS_ENDPOINT = "https://api.sheety.co/a3e86da06554d3c95d2a951fe66f4bcd/myWorkouts/workouts"
APP_ID = "6deeaf10"

SHEET_KEY = os.getenv("SHEET_KEY")
APP_KEY = os.getenv("NUTRITION_KEY")

ex_input = input("Enter your excersize information: ")

headers = {
    "x-app-key":APP_KEY,
    "x-app-id":APP_ID,
}
nut_params = {
    "query": ex_input
}

response = requests.post(NUTRITION_ENDPOINT, json=nut_params,headers=headers)

keyword_data = response.json()["exercises"][0]

today = dt.datetime.now()


sheet_params = {
    "workout": {
        "date": today.strftime("%d/%m/%Y"),
        "time": today.strftime("%H:%M:%S"),
        "exercise":keyword_data["name"],
        "duration":round(keyword_data["duration_min"]),
        "calories":round(keyword_data["nf_calories"])

    }
}
headers = {
    "content-type":"application/json",
    "Authorization": "Bearer " + SHEET_KEY
}


sheets_response = requests.post(ADD_ROW_SHEETS_ENDPOINT,json=sheet_params,headers=headers)

print(sheets_response.json())