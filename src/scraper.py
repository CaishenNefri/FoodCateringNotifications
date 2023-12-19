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

import requests
import json #needed to parse json response from Selenium Standalone Server
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


from dotenv import load_dotenv
import os

KVUri = f"https://kvzc.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

print("Load secrets from key vault")
telegram_token = client.get_secret("telegram-token").value
telegram_chat_id = client.get_secret("telegram-chat-id").value
zc_username = client.get_secret("zc-username").value
zc_password = client.get_secret("zc-password").value

telegram_message = ""
method = "sendMessage"



print("Start Chrome driver")
chrome_options = Options()
chrome_options.add_argument("--disable-dev-shm-usage")
try:
    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options) # localhost address points to Selenium Standalone Server container in the same pod where script is running
    try:
        driver.implicitly_wait(10) #setup implicit wait for whole driver

        print("Enter login page zdrowycatering.pl")
        time.sleep(5) # wait until page is loaded
        driver.get("https://panel.zdrowycatering.pl/pl/auth/login") # go to login page for zdrowycatering.pl
        time.sleep(5) # wait until page is loaded

        print("Accept cookies")
        cookies = driver.find_element(By.CLASS_NAME, "consent-give").click() #accept cookies

        print("Try to signin")
        login_form = driver.find_element(By.XPATH, "//form[1]") # find login form
        login_form.find_element(By.NAME, "username").send_keys(zc_username) # provide username
        login_form.find_element(By.NAME, "password").send_keys(zc_password) #provide password
        login_form.submit() # submit login form
        time.sleep(5) # wait until page is loaded

        print("Choose Marcin's diet")
        diets_list = driver.find_element(By.CLASS_NAME, "select--diets").click() # open menu with diets
        driver.find_element(By.XPATH, "//*[text()='Marcin (#88285) nr zamówienia (#97141)']").click() # pick Marcin's diet
        # driver.find_element(By.XPATH, "//*[text()='Paulina (#88286) nr zamówienia (#97141)']").click() # pick Paulina's diet
        time.sleep(5) # wait untl page is loaded

        print("Pick today's date")
        day = driver.find_element(By.CLASS_NAME, "DayPicker-Day.DayPicker-Day--today").click() # pick today's date

        print("Get dishes for today")
        dishes = driver.find_elements(By.CLASS_NAME, "css-kfgalm") # find all dishes for today

        print("Print all dishes for today")
        for dish in dishes:
            print(dish.text)
            telegram_message += dish.text + "\n"
        
        url = f"https://api.telegram.org/bot{telegram_token}/{method}?chat_id={telegram_chat_id}&text={telegram_message}"
        x = requests.post(url)
        print(x.text)
    finally:
        print("Failing scraping today dishes")
        driver.quit() # closes all browser windows and ends the WebDriver session
finally:
    try:
        # Try to stop Selenium container before finishing script. It finishs Container App Job fully
        print("Tring to get Selenium Standalone Server status")
        response = requests.get("http://127.0.0.1:4444/wd/hub/status")
        loaded = json.loads(response.text)
        print("Getting Selenium Node id")
        node_id = loaded["value"]["nodes"][0]["id"]
        print("Draining Selenium Node")
        requests.post(f"http://127.0.0.1:4444/se/grid/distributor/node/{node_id}/drain", headers={"X-REGISTRATION-SECRET": ""})
    finally:
        print("Closing Sellenium Standalone Server failed")
    print("End of script")
    