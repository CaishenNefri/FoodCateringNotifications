#https://panel.zdrowycatering.pl/pl/auth/login

import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys


from dotenv import load_dotenv
import os

print("Load env variables")
load_dotenv()
username = os.getenv("zc_username")
password = os.getenv("zc_password")

print("Start Chrome driver")
chrome_options = Options()
chrome_options.add_argument('--headless')
# userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
# chrome_options.add_argument(f'user-agent={userAgent}')
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Remote("http://browser:4444/wd/hub", options=chrome_options)
driver.implicitly_wait(10) #setup implicit wait for whole driver

print("Enter login page zdrowycatering.pl")
driver.get("https://panel.zdrowycatering.pl/pl/auth/login") # go to login page for zdrowycatering.pl

print("Accept cookies")
cookies = driver.find_element(By.ID, "rcc-confirm-button").click() #accept cookies

print("Try to signin")
login_form = driver.find_element(By.XPATH, "//form[1]") # find login form
login_form.find_element(By.NAME, "username").send_keys(username) # provide username
login_form.find_element(By.NAME, "password").send_keys(password) #provide password
login_form.submit() # subimt login form
time.sleep(5) # wait untl page is loaded

print("Choose Marcin's diet")
diets_list = driver.find_element(By.CLASS_NAME, "select--diets").click() # open menu to pick Marcin's diet
driver.find_element(By.XPATH, "//*[text()='Marcin (#88285) nr zamówienia (#97141)']").click() # pick Marcin's diet
time.sleep(5) # wait untl page is loaded

print("Pick today's date")
day = driver.find_element(By.CLASS_NAME, "DayPicker-Day.DayPicker-Day--today").click() # pick today's date

print("Get dishes for today")
dishes = driver.find_elements(By.CLASS_NAME, "css-kfgalm") # find all dishes for today

print("Print all dishes for today")
for dish in dishes:
    print(dish.text)
driver.close()