from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")
driver.implicitly_wait(1)
try:
    driver.find_element(By.ID,"langSelect-EN").click()
except:
    pass

cookie = driver.find_element(By.ID, "bigCookie")
total_cookies = driver.find_element(By.ID,"cookies")
# cookie_rate = WebDriverWait(driver,timeout=2).until(lambda d: d.find_element(By.ID,"cookiesPerSecond"))

cursor = driver.find_element(By.ID,"product0")
gma = driver.find_element(By.ID,"product1")
game = True
count = 0


# def upgrade():
#     if float(cookie_rate.text) == 0.0 and int(total_cookies.text) >= 15:
#         cursor.click()
#     elif float(cookie_rate.text) == 0.1 and int(total_cookies.text) >= 100:
#         driver.find_element(By.ID, "upgrade0").click()
#     elif float(cookie_rate.text) == 0.2 and int(total_cookies.text) >= 500:
#         driver.find_element(By.ID, "upgrade1").click()

# while game:
#     time.sleep(.05)
#     count += 1
#     if count == 100:
#         upgrade()
#     cookie.click()
    
driver.quit()

