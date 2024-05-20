import json
import os
import threading
import time
from multiprocessing import Pool, Lock

import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures
##############################################
from selenium import __version__ as seleniumversion
from seleniumwire import __version__ as seleniumwireversion
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
# A package to have a chromedriver always up-to-date.
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager import __version__ as webdriver_manager_version

##############################################

USERNAME = "abdel9"
PASSWORD = "Admin_2050Pass"
TARGET = "https://ip.oxylabs.io"
ENDPOINT = "pr.oxylabs.io:7777"

API_URL = "https://skeapp.jacadix.net/api/live-data"
API_Comments_URL = "https://skeapp.jacadix.net/api/comments"

CHECK_INTERVAL = 10

global bigo_accounts, bigo_comments, bigo_live, bigo_live_set
bigo_accounts = []
bigo_comments = []
bigo_live_set = set()

global driver_map
driver_map = {}

def close_unlisted_accounts(current_ids):
    global driver_map, bigo_live_set
    to_remove = []
    for account_id in bigo_live_set:
        if account_id not in current_ids:
            print(f"Closing driver for account_id: {account_id}")
            driver = driver_map.get(account_id)
            if driver:
                driver.quit()
                del driver_map[account_id]
            to_remove.append(account_id)
    for account_id in to_remove:
        bigo_live_set.remove(account_id)

def fetch_accounts(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch accounts: {response.status_code}")
        return []


def fetch_comments(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch accounts: {response.status_code}")
        return []

def update_accounts():
    global bigo_accounts, bigo_live_set, bigo_live, live_id
    accounts_data = fetch_accounts(API_URL)
    new_accounts = []
    current_ids = set()
    for account_data in accounts_data:
        account_id = account_data['id']
        current_ids.add(account_id)
        if account_id not in bigo_live_set:  # Check if the account has already been started
            bigo_live_set.add(account_id)
            bigos = json.loads(account_data['bigos'])
            live_id = account_data['live_id']
            bigo_live = account_data['live_id']
            for bigo in bigos:
                account = {
                    'phone': bigo['phone'],
                    'password': bigo['password'],
                    'country': bigo['country'],
                    'live_id': live_id,
                    'id': account_id  # Adding 'id' to the account dictionary
                }
                bigo_accounts.append(account)
                new_accounts.append(account)
    print('new accounts', new_accounts)
    return new_accounts, current_ids


def update_comments():
    comments_data = fetch_comments(API_Comments_URL)
    for comment in comments_data:
        bigo_comments.append(comment['comment'])


def delay(delay=0.2):
    time.sleep(delay)


def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
        "proxy": {
            "http": f"https://{user}:{password}@{endpoint}",
            "https": f"https://{user}:{password}@{endpoint}",
        }
    }
    return wire_options


def wait_for_element(driver, locator):
    return WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator))


def move_slider(action, track_width):
    move_step = track_width // 20  # Using smaller, more precise steps
    for i in range(25):
        action.move_by_offset(move_step, 0)  # Move horizontally without vertical deviation
        action.pause(random.uniform(0.05, 0.1))

def handle_slider_verification(driver):
    try:
        print("Verifying captcha slider...")
        slider_track = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textele"))
        )
        track_width = slider_track.size['width']

        slider_handle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-sliderele"))
        )
        action = ActionChains(driver)
        action.click_and_hold(slider_handle)

        move_slider(action, track_width)
        action.release().perform()

        captcha_text_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textelediv"))
        )
        captcha_text = captcha_text_element.text
        print("Captcha Text:", captcha_text)

        if 'failed' in captcha_text:
            print("Retrying captcha verification...")
            retry_confirm_element = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable(
                    (By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-refreshele"))
            )
            retry_confirm_element.click()
            time.sleep(2)
            handle_slider_verification(driver)

        elif 'Verification successful' not in captcha_text:
            print("Captcha verification failed.")
            driver.quit()
            return False

        print("Captcha verification successful.")
        return True

    except Exception as e:
        print(f"Error during slider verification: {e}")
        driver.quit()
        return False


def handle_account(account):
    print("handle_account started")
    global bigo_live, bigo_live_set, live_id
    bigo_phone = account['phone']
    bigo_password = account['password']
    bigo_country = account['country']
    live_id = account['live_id']
    account_id = account['id']
    print(f"Handling account with live_id: {live_id}")
    bigo_live_set.add(live_id)
    options = Options()
    print("options", bigo_live_set)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-dev-shm-usage')
    proxies = chrome_proxy(USERNAME, PASSWORD, ENDPOINT)

    print("End Options")

    print("Init Service")
    service = Service(executable_path=ChromeDriverManager().install())
    print("End Service")

    print("Init Driver")
    driver = webdriver.Chrome(
        service=service,
        options=options,
        seleniumwire_options=proxies,
        # desired_capabilities=caps
    )
    print("End Driver")

    print(f"Init Open Live {bigo_live}")
    # Open the URL
    driver.get(f"https://m.hzmk.site/{bigo_live}")
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')
    print(f"End Openninig {bigo_live}")
    try:
        try:
            print("Accept privacy")
            privacy_confirm_element = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.ID, "privacy-confirm-ele"))
            )
            privacy_confirm_element.click()
            delay()
        except:
            driver.quit()
            handle_account(account)

        print('Middle')

        try:
            close_button = WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "close"))
            )
            close_button.click()
            delay()
            print("End privacy")
        except:
            driver.quit()
            handle_account(account)

        try:
            login_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "head-right__login__btn"))
            )
            login_button.click()
            delay()
        except:
            driver.quit()
            handle_account(account)

        try:
            sign_up_link = WebDriverWait(driver, 70).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up now')]"))
            )
            sign_up_link.click()
            delay()
        except:
            driver.quit()
            handle_account(account)

        try:
            login_tab_button = WebDriverWait(driver, 90).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "tab-login-sign__item"))
            )
            login_tab_button.click()
            delay()
        except:
            driver.quit()
            handle_account(account)

        try:
            country_select_component = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".CountrySelect-Component"))
            )
            country_select_component.click()
            delay()
        except:
            driver.quit()
            handle_account(account)

        country_li = WebDriverWait(driver, 110).until(
            EC.visibility_of_element_located((By.XPATH, f"//li[contains(span/text(), '{bigo_country}')]"))
        )
        country_li.click()
        delay()

        phone_input = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".LoginForm-Component .phone-number-box input"))
        )
        phone_input.send_keys(bigo_phone)
        delay()

        password_input = WebDriverWait(driver, 130).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".LoginForm-Component .password-tab input"))
        )
        password_input.send_keys(bigo_password)
        delay()

        print("Sleep")
        time.sleep(3)
        print("Wake")

        ## Handle Slider
        handle_slider_verification(driver)

        print("login")
        time.sleep(2)
        submit_login = WebDriverWait(driver, 150).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-sumbit")))
        submit_login.click()
        print("end login")

        print("open live")
        time.sleep(2)
        textarea_present = EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
        WebDriverWait(driver, 10).until(textarea_present)
        textarea_locator = (By.CSS_SELECTOR, "textarea")
        wait_for_element(driver, textarea_locator)
        print("write comment")
        try:
            textarea = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea"))
            )
            time.sleep(1)
            random_comment = random.choice(bigo_comments)
            textarea.send_keys(random_comment)
            time.sleep(2)
            textarea.send_keys(Keys.ENTER)
            print("end write comment")
        except Exception as e:
            time.sleep(2)
            textarea = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea"))
            )
            time.sleep(1)
            random_comment = random.choice(bigo_comments)
            textarea.send_keys(random_comment)
            time.sleep(2)
            textarea.send_keys(Keys.ENTER)
            print("end write comment 2")
            print(f"Error in sending text to textarea: {str(e)}")

    except Exception as e:
        print(f"Error during execution 101: {str(e)}")

    # Final actions or cleanup
    input("Press any key to close the browser...")
    # driver.quit()

def periodic_update():
    while True:
        try:
            print("Periodic update")
            new_accounts, current_ids = update_accounts()
            if new_accounts:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    for account in new_accounts:
                        print('Starting new account:', account)
                        executor.submit(handle_account, account)
            # close_unlisted_accounts(current_ids)
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Error in periodic update: {str(e)}")
            continue


# Initial update
update_accounts()
update_comments()

print("Initial bigo_accounts:", bigo_accounts)
print("Initial bigo_comments:", bigo_comments)
print("Initial bigo_live:", bigo_live)
print("Initial bigo_accounts:", bigo_accounts)


update_thread = threading.Thread(target=periodic_update, daemon=True)
update_thread.start()

with concurrent.futures.ThreadPoolExecutor() as executor:
    for account in bigo_accounts:
        print('thread', account)
        executor.submit(handle_account, account)


