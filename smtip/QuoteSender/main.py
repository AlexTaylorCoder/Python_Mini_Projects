import datetime as dt
import smtplib
from random import randint
import calendar
from dotenv import load_dotenv
import os

load_dotenv()

my_email = os.getenv("my_email")
to_email = os.getenv("to_email")
password = os.getenv("password")


now = dt.datetime.now()
# print(now.strftime("%H:%M:%S:%MS"))
date = dt.datetime(year=1995,day=15,month=12,hour=4)


with open("quotes.txt","r") as f:
    quote = f.readlines()[randint(0,101)]
    
weekday = calendar.day_name[now.weekday()]

with smtplib.SMTP("smtp.gmail.com",port=587) as c:
    c.starttls()
    c.login(user=my_email,password=password)
    c.sendmail(
        from_addr=my_email,
        to_addrs=to_email,
        msg=f"Subject:Quote of {weekday}\n\nquote"
    )
