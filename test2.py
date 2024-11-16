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
# chrome_options.add_argument("--headless=new")
chrome_install = ChromeDriverManager().install()
folder = os.path.dirname(chrome_install)
chromedriver_path = os.path.join(folder, "chromedriver.exe")
service = ChromeService(chromedriver_path)


driver = webdriver.Chrome(service=service, options=chrome_options)

def appendProduct(file_path2, data):
    temp_file = 'temp_file.csv'
    if os.path.isfile(file_path2):
        df = pd.read_csv(file_path2, encoding='utf-8')
    else:
        df = pd.DataFrame()

    df_new_row = pd.DataFrame([data])
    df = pd.concat([df, df_new_row], ignore_index=True)

    try:
        df.to_csv(temp_file, index=False, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while saving the temporary file: {str(e)}")
        return False

    try:
        os.replace(temp_file, file_path2)
    except Exception as e:
        print(f"An error occurred while replacing the original file: {str(e)}")
        return False

    return True

def get_company_links():
    driver.get("https://www.wlw.de/de/suche?q=drechslerei&supplierTypes=Produktion")
    profile_links=[]
    time.sleep(2)
    try:
        cookie_button=driver.find_element(By.ID,"CybotCookiebotDialogFooterButtonAcceptAll")
        cookie_button.click()
        time.sleep(1)
    except:
        print("No cookie button")
        pass
    
    while True:
        company_profile_links=driver.find_elements(By.XPATH,"//a[@data-test='company-name']")
        for link in company_profile_links:
            company_link=link.get_attribute("href")
            profile_links.append(company_link)
            print(company_link)
        try:
            next_button=driver.find_element(By.XPATH,"//a[@class='button next']")
            if next_button:
                next_button.click()
                time.sleep(4)
        except:
            break
    print(f"The len of profile links are {len(profile_links)}")
    return profile_links

def scrape_data(profile_links):
    for profile in profile_links:
        driver.get(profile)
        time.sleep(1)
        try:
            cookie_button=driver.find_element(By.ID,"CybotCookiebotDialogFooterButtonAcceptAll")
            cookie_button.click()
            time.sleep(1)
        except:
            print("No cookie button")
            pass
        try:
            company_name=driver.find_element(By.TAG_NAME,"h1").text
        except:
            company_name=""
        try:
            company_location=driver.find_element(By.XPATH,"//div[@data-test='company-card']//div[@class='font-copy-400 text-navy-70 ep:text-darkgreen-70']/div[1]").text
        except:
            company_location=""
        try:
            company_origin_country=driver.find_element(By.XPATH,"//div[@data-test='company-card']//div[@class='font-copy-400 text-navy-70 ep:text-darkgreen-70']/div[2]").text
        except:
            company_origin_country=""
        try:
            website_button=driver.find_element(By.XPATH,"//button[contains(@class,'website-button')]")
            website_button.click()
            time.sleep(1)
            website_link=driver.find_element(By.XPATH,"//a[contains(@class,'website-button')]").get_attribute("href")
        except:
            website_link=""

        try:
            phone_number_button=driver.find_element(By.XPATH,"//button[contains(@class, 'phone-button')]")
            phone_number_button.click()
            time.sleep(1)
            phone_number=driver.find_element(By.XPATH,"//div[@class='tooltip light']").text
        except:
            phone_number=""
        try:
            description=driver.find_element(By.XPATH,"//div[@data-test='description']")
            try:
                more_description=driver.find_element(By.XPATH,"//div[@data-test='description']//button[.='Mehr']")
                if more_description:
                    more_description.click()
                    time.sleep(1)
            except NoSuchElementException:
                pass
            description_text=description.text
        except:
            description_text=""
        try:
            contact_person=driver.find_element(By.XPATH,"//div[contains(@class,'contacts')]//div[@class='name font-semibold']").text
        except:
            contact_person=""
        try:
            contact_person_phone_button=driver.find_element(By.XPATH,"//div[contains(@class,'contacts')]//button[contains(@class,'phone-button')]")
            driver.execute_script("arguments[0].scrollIntoView();",contact_person_phone_button)
            time.sleep(1)
            contact_person_phone_button.click()
            time.sleep(1)
            contact_person_phone_number=driver.find_element(By.XPATH,"//div[@class='tooltip light']").text
        except:
            contact_person_phone_number=""
        data={
            "Company Name":company_name,
            "Company Location":company_location,
            "Country":company_origin_country,
            "Website Link":website_link,
            "Phone Number":phone_number,
            "Description":description_text,
            "Contact Person":contact_person,
            "Contact Person's Phone":contact_person_phone_number
        }
        print(data)
        appendProduct("drechslerei_wlw_data.csv",data)

    driver.quit()
        

# drechslerei_links=get_company_links()
# for link in drechslerei_links:
#     f=open("drechslerei_links.txt","a")
#     f.write(f"{link}\n")

profile_links=[]
f=open("drechslerei_links.txt","r")
for link in f:
    profile_links.append(link.split("\n")[0])
print(profile_links)
scrape_data(profile_links)