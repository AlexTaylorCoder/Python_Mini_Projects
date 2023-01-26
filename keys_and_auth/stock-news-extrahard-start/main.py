import os
import datetime as dt
import requests
from dotenv import load_dotenv
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
HOURS_IN_DAY = 24

load_dotenv()

STOCK_AUTH = os.getenv("STOCK_AUTH")
NEWS_AUTH = os.getenv("NEWS_AUTH")
TRELLO_AUTH = os.getenv("TRELLO_AUTH")
ACCOUNT_SID = "AC46488998e7476f389f1cb0eecbe75e23"

today = dt.datetime.today()
yesterday = today - dt.timedelta(days=2)
before_yesterday = yesterday - dt.timedelta(days=1)

stock_params = {
    "apikey":STOCK_AUTH,
    "function":"TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval":"60min"
}
news_params = {
    "apiKey":NEWS_AUTH,
    "q":"Tesla",
    "from":yesterday,
    "to":today,
    "language":"en",
    "pageSize":3

}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

def avg_hourly(stock_data,key):
    return (float(stock_data[key]["3. low"]) + float(stock_data[key]["2. high"])) / 2

def find_stock():
    response = requests.get("https://www.alphavantage.co/query?",params=stock_params)
    response.raise_for_status()
    stock_data = response.json()["Time Series (60min)"]
    sum_yesterday = 0
    sum_before_yesterday = 0
    for key in stock_data:
        if str(yesterday.day) in key:
            sum_yesterday += avg_hourly(stock_data,key)
        elif str(before_yesterday.day) in key:
            sum_before_yesterday += avg_hourly(stock_data,key)

    avg_yesterday_daily = sum_yesterday / 24
    avg_before_yesterday_daily = sum_before_yesterday / 24
    diff = avg_yesterday_daily - avg_before_yesterday_daily
    if diff >= 1:
        find_news(f"{STOCK}: 🔺{round(diff,2)}%\n")
    elif -1 >= diff:
        find_news(f"{STOCK}: 🔻{round(diff,2)}%\n")


            

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

def find_news(format_str):
    response = requests.get("https://newsapi.org/v2/everything",params=news_params)
    response.raise_for_status()
    news_data = response.json()["articles"]
    for articles in news_data:
        descr = articles["description"]
        content = articles["content"]
        if len(descr) > 30:
            i = descr.index(".")
            descr = descr[:i]
        if len(content) > 150:
            for i in range(150,200):
                if content[i] == ".":
                    content = content[:i]
                    break
            else:
                content = content[:200]
        format_str += f'\n\nHeadline: {descr}\nBrief: {content}\nLink:{articles["url"]}'
    send_msg(format_str)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

def send_msg(format_str):
    client = Client(ACCOUNT_SID, TRELLO_AUTH)
    message = client.messages.create(
        body=format_str,
        from_= "+19405319275",
        to = "+19178064701"
        )
    print(message.status)

find_stock()
#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
