##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import datetime as dt
import pandas as pd
from random import randint
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

my_email = os.getenv("my_email")
password = os.getenv("password")
to_email = os.getenv("to_email")

#Query database
now = dt.datetime.now()
df = pd.read_csv("birthdays.csv")
birthday_user = df[(df["month"] == now.month) & (df["day"] == now.day)]
if not birthday_user.empty:
    name = birthday_user.name[1]
    sending_to = birthday_user.email[1]

    #Open letter template

    with open(f"./letter_templates/letter_{randint(1,3)}.txt") as f:
        message = ''.join(f.readlines())

    updated_message = message.replace("[NAME]",name)

    with smtplib.SMTP("smtp.gmail.com",port=587) as c:
        c.starttls()
        c.login(user=my_email, password=password)
        c.sendmail(from_addr=my_email,to_addrs=to_email,msg=f"Subject:Happy Birthday {name}!\n\n{updated_message}")

