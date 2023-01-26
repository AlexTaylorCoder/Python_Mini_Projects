import requests
import smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()


EMAIL = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


AMAZON_ENDPOINT = "https://www.amazon.com/Pink-Miracle-Cleaner-Leather-Sneakers/dp/B00A7NDT3A/ref=sxin_15_pa_sp_search_thematic_sspa?content-id=amzn1.sym.a5710394-3d57-4d27-93ab-3d4a038712c2%3Aamzn1.sym.a5710394-3d57-4d27-93ab-3d4a038712c2&cv_ct_cx=shoe%2Bcleaner&keywords=shoe%2Bcleaner&pd_rd_i=B00A7NDT3A&pd_rd_r=38c9a2eb-2420-4f92-bfc0-2d6e466684e0&pd_rd_w=PgJSS&pd_rd_wg=ql1n0&pf_rd_p=a5710394-3d57-4d27-93ab-3d4a038712c2&pf_rd_r=XK7Y1KZ6X8KDA3PFZ23D&qid=1674507834&s=home-garden&sprefix=shoe%2Bcl%2Cgarden%2C76&sr=1-1-3bc0c0df-c7bd-4bd8-89e8-c7f4dd05d048-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzSjFHMDFRSkFKMEZEJmVuY3J5cHRlZElkPUEwMTg5MzQwMUxYTlZNTVlOQUZIRyZlbmNyeXB0ZWRBZElkPUEwMDQzNjAzMktQVU41VkhPREhMOSZ3aWRnZXROYW1lPXNwX3NlYXJjaF90aGVtYXRpYyZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1&psc=1"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
response = requests.get(AMAZON_ENDPOINT,headers=headers)

response.raise_for_status()
amazon_data = response.text

soup = BeautifulSoup(amazon_data,"html.parser")

price = soup.select("#apex_desktop .a-section .a-price .a-offscreen")[0].text
name = soup.select("#titleBlock #titleSection #title #productTitle")[0].text

float_price = float(price[1:])

with smtplib.SMTP("smtp.gmail.com",port=587) as c:
    c.starttls()
    c.login(user=EMAIL,password=password)
    c.sendmail(
        from_addr=EMAIL,
        to_addrs="alextaylor515@gmail.com",
        msg=f"Subject: Alert: {name} is now at a price of {price}\n\n {name} is now in your pricerange. Purchase soon"
    )
