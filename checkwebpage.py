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



cservice = webdriver.ChromeService('C:/Users/lsywu/OneDrive/Documents/SMU/bbdc-booking-bot/chromedriver-win64/chromedriver.exe') 
browser = webdriver.Chrome(service = cservice)
def check_webpage():
    #on webpage, try to find the element 
    try:
        browser.find_element(By.CLASS_NAME,"calendar")
    except:
        return False
    else: 
        return True
    
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
config = load_config("config.yaml")

def check_slots(month):
    #finding the month button           
    month = config["months"]["month"]
    try:
        browser.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[2]/button[1] and contains(.,"{month}")')
    #cannot find
    except:
        print("The month of {month} has no free slots.")
        return False
    #found slots   
    else:
        print("The month of {month} has free slots")
        try:
            browser.find_element(By.CLASS_NAME,"v-btn v-btn--is-elevated v-btn--fab v-btn--has-bg v-btn--round theme--light v-size--default primary active-btn")
        except:
            print("There are no free slots")
            return False
        else:
            print("There are free slots")
            return True
       

        


    


    