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
from checkwebpage import check_webpage, check_slots
from bookslot import book_slot

# setup logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

def app(config):
    cservice = webdriver.ChromeService('C:/Users/lsywu/OneDrive/Documents/SMU/bbdc-booking-bot/chromedriver-win64/chromedriver.exe') 
    browser = webdriver.Chrome(service = cservice)
    #1. check whether webpage has element calendar
    correct_webpage = check_webpage()
    if correct_webpage:
        checking = check_slots()
        while checking == False:
            #refreshing the page
            browser.navigate().refresh()
        book_slot()
        #send_confirmation_msg()
    else:
        pass


    # Switching back to Main Frame and pressing 'I Accept'
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        browser.find_element_by_name('mainFrame')))
    wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "btn"))).click()

    # Selection menu
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        browser.find_element_by_name('mainFrame')))
    wait.until(EC.visibility_of_element_located((By.ID, "checkMonth")))

    # 0 refers to first month, 1 refers to second month, and so on...
    months = browser.find_elements_by_id('checkMonth')
    if len(months) == 13:
        months[12].click()  # all months
    else:
        months[0].click()  # first month

    # 0 refers to first session, 1 refers to second session, and so on...
    sessions = browser.find_elements_by_id('checkSes')
    sessions[8].click()  # all sessions

    # 0 refers to first day, 1 refers to second day, and so on...
    days = browser.find_elements_by_id('checkDay')
    days[7].click()  # all days

    # Selecting Search
    browser.find_element_by_name('btnSearch').click()

    # Dismissing Prompt
    wait = WebDriverWait(browser, 15)
    wait.until(EC.alert_is_present())
    alert_obj = browser.switch_to.alert
    alert_obj.accept()

    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "slot")))
    except TimeoutException:
        logging.info("no slot is available")
        browser.quit()
        return

    logging.info("find available slots")
    wanted = []
    # 0 refers to first slot, 1 refers to second slot, and so on...
    slots = browser.find_elements_by_name('slot')
    logging.info(f"number of slot: {len(slots)}")
    for slot in slots:     # Selecting all checkboxes
        # parse the data
        parent = slot.find_element_by_xpath('./..')
        text = parent.get_attribute("onmouseover")
        splits = text.split(",")
        session_date = splits[2].replace('"', '')
        session_id = splits[3].replace('"', '')
        session_start_time = splits[4].replace('"', '')
        session_end_time = splits[5].replace('"', '')

        logging.info(
            f"session availabile:    date:{session_date}, slot:{session_id}, time:{session_start_time}-{session_end_time}")
        if session_id in want_sessions:
            wanted.append({"check": slot, "date": session_date, "slot": session_id,
                          "start_time": session_start_time, "end_time": session_end_time})

    logging.info(f"number of wanted slot: {len(wanted)}")

    # send notification by telegram if any available slot
    if len(wanted) > 0 and enable_bot:
        message = "session availabile:"
        for sess in wanted:
            date = sess["date"]
            slot = sess["slot"]
            start, end = sess["start_time"], sess["end_time"]
            message += f"\ndate:{date}, slot:{slot}, time:{start}-{end}"
        send_message(message, bot_token, chat_id)

        # # Uncomment the below code to book the first available slot
        # # select the first one and submit
        # wanted[0]['check'].click()
        # # clicking random element to hide hover effect
        # browser.find_element_by_class_name('pgtitle').click()
        # # Selecting Submit
        # browser.find_element_by_name('btnSubmit').click()
        # # Selecting confirm
        # wait.until(EC.visibility_of_element_located(
        #     (By.XPATH, "//input[@value='Confirm']")))
        # browser.find_element_by_xpath("//input[@value='Confirm']").click()

    browser.quit()

