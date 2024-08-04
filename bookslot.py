import sys
import time
from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import load_config
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
config = load_config("config.yaml")

cservice = webdriver.ChromeService('C:/Users/lsywu/OneDrive/Documents/SMU/bbdc-booking-bot/chromedriver-win64/chromedriver.exe') 
browser = webdriver.Chrome(service = cservice)
def book_slot():
    #select the month
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    config = load_config("config.yaml")
    month = config["months"]["month"]
    mthbtn = browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[2]/button[1] and contains(.,"{month}")')
    mthbtn.click()
    #select the date
    datebtn = browser.find_element(By.XPATH,'//*[@id="app"]/div/div/main/div/div/div[3]/div/div[1]/div[1]/div[4]/div/div/div/div[2]/div[5]/div/button')
    datebtn.click()
    #select the slot
