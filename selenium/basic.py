from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.python.org/")

menu = driver.find_elements(By.CSS_SELECTOR,"#content > div > section > div.list-widgets.row > div.medium-widget.event-widget.last > div ul li")

events = {}

count = 0
for item in menu:
    time = item.find_element(By.CSS_SELECTOR,"time").text
    event_name = item.find_element(By.CSS_SELECTOR,"a").text
    events[count] = {"time":time, "name":event_name}
    count += 1 

print(events) 