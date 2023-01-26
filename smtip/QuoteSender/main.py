import datetime as dt
import smtplib
from random import randint
import calendar

my_email = "pythontestuser515@gmail.com"
password = "dbcuwleosfqrrydr"

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
        to_addrs="alextaylor515@gmail.com",
        msg=f"Subject:Quote of {weekday}\n\nquote"
    )
