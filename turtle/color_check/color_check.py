# from colorgram import extract
from bs4 import BeautifulSoup as bs
import colorgram
import requests


keywords = input("Enter keywords: ").strip()

keywords = keywords.replace(" ","+")



data = requests.get(f"https://www.google.com/search?q={keywords}&tbm=isch&sclient=img").text


soup = bs(data,'html.parser')
# relavant = soup.find('div',jsname="r5xl4")
print(soup)
images = soup.select(".jB2rPd")

print(images)
colors = []

for image in images:
    src = image['src']
    colors.append(colorgram.extract(src,6))

print(colors)