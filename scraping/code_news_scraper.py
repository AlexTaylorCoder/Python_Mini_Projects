from bs4 import BeautifulSoup
import requests

#First and second TR then skip third

NEWS_URL = "https://news.ycombinator.com/"

response = requests.get(NEWS_URL)

data = response.text

soup = BeautifulSoup(data,"html.parser")

content = soup.select("table:not(#hnmain) tr:not(.spacer):not(.morespace)")

titles = []
links = []
scores = []

for i,item in enumerate(content):
    if i % 2:
        link_content = item.select_one(".title .titleline a")
        # text = link_content.text
        # link = link_content.get("href")
        if link_content:
            titles.append(link_content.text)
            links.append(link_content.get("href"))
    else:
        if i != 0 and i != len(content)-1:
            score = item.select_one(".score")
            if score:
                scores.append(int(score.text.split()[0]))
            else:
                scores.append(0)


largest = 0
index = 0
for i,s in enumerate(scores):
    if s > largest:
        largest = s
        index = i


print(titles[index])
print(links[index])





