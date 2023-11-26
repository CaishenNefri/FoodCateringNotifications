#https://panel.zdrowycatering.pl/pl/auth/login

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys
chrome_options = Options()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(10) #setup implicit wait for whole driver


driver.get("https://panel.zdrowycatering.pl/pl/auth/login") # go to login page for zdrowycatering.pl
cookies = driver.find_element(By.ID, "rcc-confirm-button").click() #accept cookies


username = "123"
password = "123"

login_form = driver.find_element(By.XPATH, "//form[1]") # find login form
login_form.find_element(By.NAME, "username").send_keys(username) # provide username
login_form.find_element(By.NAME, "password").send_keys(password) #provide password
login_form.submit() # subimt login form

diets_list = driver.find_element(By.CLASS_NAME, "select--diets").click() # open menu to pick Marcin's diet
driver.find_element(By.XPATH, "//*[text()='Marcin (#88285) nr zamówienia (#97141)']").click() # pick Marcin's diet
time.sleep(5) # wait untl page is loaded

day = driver.find_element(By.CLASS_NAME, "DayPicker-Day.DayPicker-Day--today").click() # pick today's date
dishes = driver.find_elements(By.CLASS_NAME, "css-kfgalm") # find all dishes for today

# print all dishes for today
for dish in dishes:
    print(dish.text)