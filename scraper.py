from seleniumwire import webdriver  # Import from seleniumwire
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv

load_dotenv()


proxy = os.getenv("PROXY_SERVER")  
username = os.getenv("PROXY_USERNAME")  
password = os.getenv("PROXY_PASSWORD")  


proxy_options = {
    'proxy': {
        'http': f'http://{username}:{password}@{proxy}',
        'https': f'https://{username}:{password}@{proxy}',
        'no_proxy': 'localhost,127.0.0.1'  
    }
}

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_install = ChromeDriverManager().install()
folder = os.path.dirname(chrome_install)
chromedriver_path = os.path.join(folder, "chromedriver.exe")
service = ChromeService(chromedriver_path)


driver = webdriver.Chrome(service=service, options=chrome_options, seleniumwire_options=proxy_options)

def get_profile_links():
    driver.get("https://www.techpilot.net/")
    time.sleep(50)
    driver.quit()

get_profile_links()