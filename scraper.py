# from seleniumwire import webdriver  
import time
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
import threading
load_dotenv()


proxy_ip = os.getenv("PROXY_SERVER")  
# username = os.getenv("PROXY_USERNAME")  
# password = os.getenv("PROXY_PASSWORD")
techpilot_username = os.getenv("TECHPILOT_USERNAME")
techpilot_password = os.getenv("TECHPILOT_PASSWORD")  


# proxy_options = {
#     'proxy': {
#         'http': f'http://{username}:{password}@{proxy}',
#         'https': f'https://{username}:{password}@{proxy}',
#         'no_proxy': 'localhost,127.0.0.1'  
#     }
# }

proxy=Proxy()
proxy.proxy_type=ProxyType.MANUAL
proxy.http_proxy=proxy_ip
proxy.ssl_proxy=proxy_ip


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument(f'--proxy-server={proxy_ip}')
# chrome_options.add_argument('--window-size=1920,1080')
chrome_install = ChromeDriverManager().install()
folder = os.path.dirname(chrome_install)
chromedriver_path = os.path.join(folder, "chromedriver.exe")
service = ChromeService(chromedriver_path)


driver = webdriver.Chrome(service=service, options=chrome_options)

def close_chatbox():
    while True:
        try:
            chatbox = driver.find_element(By.XPATH, "//div[@class='olark-size-md']")
            if chatbox:
                close_chatbox_button = driver.find_element(By.XPATH, "//button[@aria-label='close chatbox']")
                close_chatbox_button.click()
                time.sleep(1)
        except:
            pass
        time.sleep(1)  

def get_profile_links():
    chatbox_thread = threading.Thread(target=close_chatbox, daemon=True)
    chatbox_thread.start()
    
    driver.get("https://www.techpilot.net/")
    time.sleep(3)
    
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']")
        cookie_button.click()
        time.sleep(1)
    except:
        pass
    
    menu = driver.find_element(By.XPATH, "//div[@id='menueNavBtn']")
    menu.click()
    time.sleep(1)
    
    login_button = driver.find_element(By.XPATH, "(//div[@data-refid='loginButton'])[2]")
    login_button.click()
    time.sleep(5)
    
    username_input = driver.find_element(By.XPATH, "//input[@id='logname']")
    password_input = driver.find_element(By.XPATH, "//input[@id='password']")
    for char in techpilot_username:
        username_input.send_keys(char)
        time.sleep(0.5)
    for char in techpilot_password:
        password_input.send_keys(char)
        time.sleep(0.5)
    
    login_now_button = driver.find_element(By.XPATH, "//div[@id='login-button']")
    login_now_button.click()
    time.sleep(5)
    driver.quit()

get_profile_links()