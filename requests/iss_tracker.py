import requests
import datetime as dt
import smtplib

USER = "pythontestuser515@gmail.com"
PASS = "dbcuwleosfqrrydr"
#Add email functionality

CURRENT_LAT = 40.791856
CURRENT_LNG = -73.972413

params = {
    "lat":CURRENT_LAT,
    "lng":CURRENT_LNG
}
def iss_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    lat = data['iss_position']['latitude']
    lng = data['iss_position']['longitude']

    if CURRENT_LAT - 2 < float(lat) < CURRENT_LAT + 2 and CURRENT_LNG - 2 < float(lng) < CURRENT_LNG + 2:
        return True
    else:
        return False

def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json",params=params)
    response.raise_for_status()
    data = response.json()
    # sunrise = int(data["results"]["sunrise"][1].split(":")[0])
    sunset = int(data["results"]["sunset"][0])
    hour = dt.datetime.now().hour
    if dt.datetime.now().minute > 30:
        hour += 1
    if hour > sunset:
        return True
    else:
        return False
    

def main():
    if is_night():
        if iss_location():
            with smtplib.SMTP("smtp.gmail.com",port=587) as c:
                c.starttls()
                c.login(user=USER,password=PASS)
                c.sendmail(
                    from_addr=USER,
                    to_addrs="alextaylor515@gmail.com",
                    msg=f"Subject:ISS is overhead\n\nLook up!\n The internation space station is overhead!"
                )
        else:
            print("The ISS is not overhead!")
    else:
        print("It's not night yet, the ISS cannot be viewed overhead")

main()