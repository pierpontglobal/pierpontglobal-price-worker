from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import json

class PriceWorker:
    driverSession = None

    def __init__(self):
        print('Initiating worker')
    
    def __call__(self):
        print('Making class')

    def human_type(self, element, text):
        element.click()
        for char in text:
            time.sleep(random.randint(1,2)/70.0)
            element.send_keys(char)

    def get_mmr(self, data_message, ws):
        if self.driverSession is None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--window-size=1920,1080')
	    chrome_options.add_argument('--no-sandbox')
	    chrome_options.add_argument('--disable-dev-shm-usage')
            self.driverSession = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
            self.driverSession.get("https://www.manheim.com/login?WT.svl=m_uni_hdr")

            usernameElement = self.driverSession.find_element_by_id("user_username")
            passwordElement = self.driverSession.find_element_by_id("user_password")
            loginbutton = self.driverSession.find_element_by_name("submit")

            self.human_type(usernameElement, 'pierpontllc')
            self.human_type(passwordElement, 'Kittie123!')
            loginbutton.click()
        
        VIN = data_message['vin']
        timeout = 5
        element_present = EC.presence_of_element_located((By.NAME, 'searchTerms'))
        WebDriverWait(self.driverSession, timeout).until(element_present)

        searchElement = self.driverSession.find_element_by_name("searchTerms")
        self.human_type(searchElement, VIN)
        time.sleep(random.randint(1,2)/30.0)
        searchElement.send_keys(Keys.ENTER)

        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'mmr-valuation'))
        WebDriverWait(self.driverSession, timeout).until(element_present)

        mmrElement = self.driverSession.find_element_by_class_name("mmr-valuation").find_element_by_tag_name('a').text

        response_data = {}
        response_data["command"] = 'message'
        response_data["identifier"] = "{\"channel\": \"PriceQueryChannel\"}"
        response_data["data"] = "{\"action\": \"update_status\", \"vin\": \""+ data_message['vin'] +"\", \"mmr\": \""+ mmrElement +"\", \"user\": \""+ str(data_message['user_id']) +"\"}"
        response_json = json.dumps(response_data)
        print response_json
        ws.send(response_json)
