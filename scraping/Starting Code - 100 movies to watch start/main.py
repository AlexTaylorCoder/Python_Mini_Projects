import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

response = requests.get(URL)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data,"html.parser")

headers = soup.select("h2")

print(headers)

