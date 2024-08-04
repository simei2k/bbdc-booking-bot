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
from bot import send_message,send_photo,get_message,get_update
import logging
import base64
import requests


# setup logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

def log_in(config):
    # username password
    username = config["bbdc"]["username"]
    password = config["bbdc"]["password"]

    # bot
    bot_token = config["telegram"]["token"]
    chat_id = config["telegram"]["chat_id"]

    # chrome host
    chrome_host = config["chromedriver"]["host"]

    # connect to chrome
    cservice = webdriver.ChromeService('C:/Users/lsywu/OneDrive/Documents/SMU/bbdc-booking-bot/chromedriver-win64/chromedriver.exe') 
    browser = webdriver.Chrome(service = cservice)
    browser.get('https://booking.bbdc.sg/#/booking/practical')

    # login BBDC
    idLogin = browser.find_element(By.ID,'input-8')
    idLogin.send_keys(username)
    idLogin = browser.find_element(By.ID,'input-15')
    idLogin.send_keys(password)
    loginButton = browser.find_element(By.XPATH,'//button[@class="v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default primary"]')
    loginButton.click()

    #finding captcha image and sending to telegram
    browser.switch_to.default_content()
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME,'v-responsive__content')))
    browser.save_screenshot("image.png")
    filelocation = "C:/Users/lsywu/OneDrive/Documents/SMU/bbdc-booking-bot/image.png"
    send_photo(filelocation,chat_id,bot_token)

    #typing message into telegram and getting the message
    time.sleep(5)
    #5 seconds to view captcha and send back
    captcharesp = get_update(bot_token)
    captcharesp = captcharesp.json()['result'][0]['message']['text']
    
    #keying in captcha into the box
    captcha = browser.find_element(By.ID,'input-30')
    captcha.send_keys(captcharesp)
    captchabtn = browser.find_element(By.XPATH,'//*[@id="app"]/div/div/div[1]/div/div/form/div/div[4]/button')
    captchabtn.click()

    #clicking book slot
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/main/div/div/div[2]/div/div[1]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div/div/button'))).click()

    #clicking without fixed instructor
    browser.switch_to.default_content()
    time.sleep(5)
    pass 