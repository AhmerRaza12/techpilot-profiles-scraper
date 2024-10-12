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
        time.sleep(0.1)
    for char in techpilot_password:
        password_input.send_keys(char)
        time.sleep(0.1)
    
    login_now_button = driver.find_element(By.XPATH, "//div[@id='login-button']")
    login_now_button.click()
    time.sleep(10)
    
    advanced_search = driver.find_element(By.XPATH, "//div[@data-tour-step='buyer-supplier-search']")
    advanced_search.click()
    
    searching_frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='legacy-iframe']")))
    driver.switch_to.frame(searching_frame)
    
    search_input = driver.find_element(By.XPATH, "//input[@onkeyup='checkEventJSP(this);']")
    search_keyword = "spanabhebende bearbeitung"
    for key in search_keyword:
        search_input.send_keys(key)
        time.sleep(0.1)
    search_input.send_keys(Keys.ENTER)
    time.sleep(7)
    
    box_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='buttonResultTypeRaster']")))
    box_results.click()
    time.sleep(4)
    

    for _ in range(140):
        try:
            next_button = driver.find_element(By.XPATH, "//div[@class='loadNextBtn']/span")
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.click()
            time.sleep(7)
        except:
            break  
    
    profile_links = []
    
    profiles = driver.find_elements(By.XPATH, "//div[contains(@class,'result_raster_cell')]")
    for profile in profiles:
        try:
            onclick_attr = profile.get_attribute('onclick')
            link_start = onclick_attr.find("window.open('") + len("window.open('")
            link_end = onclick_attr.find("','_blank'")
            profile_link = onclick_attr[link_start:link_end]
            profile_links.append(profile_link)
        except:
            continue
    
    with open("profile_links.txt", "w") as f:
        for link in profile_links:
            f.write(link + "\n")
    
    print(f"Extracted {len(profile_links)} profile links.")
    driver.quit()


get_profile_links()
def get_data(profiles):
        for profile in profiles[:5]:
            profile.click()
            time.sleep(10)
            driver.switch_to.window(driver.window_handles[1])
            show_phone_numbers= driver.find_elements(By.XPATH, "//span[@class='phonePlaceholder']")
            for show_phone_number in show_phone_numbers:
                show_phone_number.click()
                time.sleep(1)
            try:    
                company_name=driver.find_element(By.XPATH, "//h1").text
            except:
                company_name=""
            try:
                company_addr=driver.find_element(By.XPATH, "//div[@id='labelAddress']/ul").text
            except:
                company_addr=""
            try:
                company_contact=driver.find_element(By.XPATH, "//div[@id='labelAddress']/ul").text
            except:
                company_contact=""
            try:
                company_data=driver.find_element(By.XPATH, "(//div[@id='labelCompData']/ul)[2]").text
            except:
                company_data=""
            try:
                company_location=driver.find_element(By.XPATH, "//div[@id='locationMap']/a").get_attribute("href")
            except:
                company_location=""
            try:
                other_locations=driver.find_element(By.XPATH, "//div[@id='furtherLocations']").text
            except:
                other_locations=""
            file_downloads,technologies=[],[]
            try:
                download_files=driver.find_elements(By.XPATH, "//div[@id='documentDownloads']//a")
                for download_file in download_files:
                    download_file_href=download_file.get_attribute("href")
                    file_downloads.append(download_file_href)
            except:
                pass
    
            try:
                company_contact_persons=driver.find_element(By.XPATH, "//div[@id='perfectContactPerson']").text
            except:
                company_contact_persons=""
            try:
                other_technologies_readmore=driver.find_element(By.XPATH, "//div[@id='perfectTechnology']/div[@class='readMore']")
                other_technologies_readmore.click()
                time.sleep(1)
                other_technologies=driver.find_elements(By.XPATH, "//div[@id='perfectTechnology']//h3")
                for other_technologie in other_technologies:
                    technologies.append(other_technologie.text)
            except:
                pass
            try:
                company_materials=driver.find_element(By.XPATH, "//div[@id='perfectMaterials']").text
            except:
                company_materials=""
            try:
                company_industries=driver.find_element(By.XPATH, "//div[@id='perfectIndustry']").text
            except:
                company_industries=""
            try:
                company_references=driver.find_element(By.XPATH, "//div[@id='perfectReferences']").text
            except:
                company_references=""
            machines_data=[]
            try:
                machines_data_elements = driver.find_elements(By.XPATH, "//div[@class='rssTpSliderBox']")
                for machine_data_element in machines_data_elements:
                    company_machine = driver.execute_script("return arguments[0].textContent", machine_data_element)
                    cleaned_machine = company_machine.replace("\n", " ").replace("\t", "").strip()
                    if '.jpg' not in cleaned_machine:
                        machines_data.append(cleaned_machine)
            except:
                pass
            data={
                "Company Name":company_name,
                "Company Address":company_addr,
                "Company Contact":company_contact,
                "Company Data":company_data,
                "Company Location":company_location,
                "Other Locations":other_locations,
                "File Download Links":"\n".join(file_downloads),
                "Company Contact Persons":company_contact_persons,
                "Technologies used":"\n".join(technologies),
                "In use Materials":company_materials,
                "Industries":company_industries,
                "References":company_references,
                "Machines":"\n".join(machines_data)
            }
            print(data)
            appendProduct("techpilot_data.csv",data)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
            searching_frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='legacy-iframe']")))
            driver.switch_to.frame(searching_frame)

driver.quit()