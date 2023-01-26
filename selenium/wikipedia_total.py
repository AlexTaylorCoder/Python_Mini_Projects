from selenium import webdriver
from selenium.webdriver.common.by import By 
from html import unescape

driver = webdriver.Chrome()
driver.get("https://en.wikipedia.org/wiki/Main_Page")

unformatted_text = driver.find_element(By.CSS_SELECTOR,"#articlecount > a:nth-child(1)").text
formatted_text = unescape(unformatted_text)
print(formatted_text)

driver.close()