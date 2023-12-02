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

import requests
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
container_app_fqdn = client.get_secret("container-app-fqdn").value
zc_username = client.get_secret("zc-username").value
zc_password = client.get_secret("zc-password").value

telegram_message = ""
method = "sendMessage"



print("Start Chrome driver")
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
# userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
# chrome_options.add_argument(f'user-agent={userAgent}')
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
try:
    driver = webdriver.Remote(f"https://{container_app_fqdn}/wd/hub", options=chrome_options)
    # driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
    # driver = webdriver.Remote("http://browser:4444/wd/hub", options=chrome_options)
    try:
        driver.implicitly_wait(10) #setup implicit wait for whole driver

        print("Enter login page zdrowycatering.pl")
        time.sleep(5) # wait untl page is loaded
        driver.get("https://panel.zdrowycatering.pl/pl/auth/login") # go to login page for zdrowycatering.pl
        time.sleep(5) # wait untl page is loaded

        print("Accept cookies")
        cookies = driver.find_element(By.ID, "rcc-confirm-button").click() #accept cookies

        print("Try to signin")
        login_form = driver.find_element(By.XPATH, "//form[1]") # find login form
        login_form.find_element(By.NAME, "username").send_keys(zc_username) # provide username
        login_form.find_element(By.NAME, "password").send_keys(zc_password) #provide password
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
            telegram_message += dish.text + "\n"
        
        url = f"https://api.telegram.org/bot{telegram_token}/{method}?chat_id={telegram_chat_id}&text={telegram_message}"
        x = requests.post(url)
        print(x.text)
    finally:
        driver.quit() # closes all browser windows and ends the WebDriver session
finally:
    print("End of script")
    