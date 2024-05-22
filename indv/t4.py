import json
import threading
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import concurrent.futures

##############################################
# from selenium import __version__ as seleniumversion
# from seleniumwire import __version__ as seleniumwireversion
# from selenium.webdriver.chrome.service import Service
# from seleniumwire import webdriver
# # A package to have a chromedriver always up-to-date.
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager import __version__ as webdriver_manager_version
##############################################


API_URL = "https://skeapp.jacadix.net/api/live-data"
BASE_URL = "https://skeapp.jacadix.net/api"
API_Comments_URL = "https://skeapp.jacadix.net/api/comments"

CHECK_INTERVAL = 10

global bigo_comments, bigo_live
bigo_live=""
bigo_comments = []


main_phone = "1068446563"
account = {
        'phone': "1068446563",
        'password': "m3290900a",
        'country': 'Egypt',
}


def post_comment(driver, bigo_comments):
    try:
        time.sleep(2)
        textarea_locator = (By.CSS_SELECTOR, "textarea")

        # Wait for the textarea to be present and visible
        textarea = wait_for_element(driver, textarea_locator)

        print("write comment")
        time.sleep(1)

        # Choose a random comment and post it
        random_comment = random.choice(bigo_comments)
        textarea.send_keys(random_comment)
        time.sleep(2)
        textarea.send_keys(Keys.ENTER)

        print("end write comment")
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_comments(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch accounts: {response.status_code}")
        return []

def get_live_by_phone(phone):
    response = requests.get(f"{BASE_URL}/live-phone", params={'phone': phone})
    return response.json()

def update_accounts(driver):
    global bigo_live
    data = get_live_by_phone(main_phone)

    if 'success' in data and data['success'] == False:
        delay(5)
        update_accounts(driver)
        return "Account not found"

    new_live_id = data['live_id']

    if new_live_id != bigo_live:
        driver.get(f"https://m.hzmk.site/{new_live_id}")
        time.sleep(3)

    bigo_live = new_live_id

    account = {
        'phone': data['phone'],
        'password': data['password'],
        'country': data['country'],
        'live_id': data['live_id']
    }

    return account

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
    print("WIDCTH: ** ", track_width)
    move_step = track_width // 15  # Using smaller, more precise steps
    step = 0.1
    print("move_step** ", move_step)
    print("step** ", step)
    for i in range(25):
        action.move_by_offset(move_step, 0)  # Move horizontally without vertical deviation
        action.pause(step)
        # action.pause(random.uniform(0.05, 0.1))
        # action.pause(0.15)
        delay(0.01)


def handle_slider_verification(driver, max_retries=4):
    retry_count = 0
    while retry_count < max_retries:
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
                print("Captcha verification failed, retrying...")
                retry_count += 1
                if retry_count < max_retries:
                    retry_confirm_element = WebDriverWait(driver, 40).until(
                        EC.element_to_be_clickable(
                            (By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-refreshele"))
                    )
                    retry_confirm_element.click()
                    time.sleep(2)
                else:
                    print("Reached maximum retries. Exiting.")
                    driver.quit()
                    handle_account(driver, account)
                    return False
            elif 'Verification successful' in captcha_text:
                print("Captcha verification successful.")
                return True
            else:
                print("Unknown captcha result, retrying...")
                retry_count += 1
                if retry_count < max_retries:
                    retry_confirm_element = WebDriverWait(driver, 40).until(
                        EC.element_to_be_clickable(
                            (By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-refreshele"))
                    )
                    retry_confirm_element.click()
                    time.sleep(2)
                else:
                    print("Reached maximum retries. Exiting.")
                    driver.quit()
                    handle_account(driver, account)
        except Exception as e:
            print(f"Error during slider verification attempt {retry_count + 1}: {e}")
            retry_count += 1
            if retry_count >= max_retries:
                print("Reached maximum retries due to exceptions. Exiting.")
                driver.quit()
                handle_account(driver, account)
                return False
    print("Captcha verification process completed with failures.")
    driver.quit()
    handle_account(driver, account)
    return False


def handle_account(driver, account):
    print("handle_account started")
    global bigo_live
    bigo_phone = account['phone']
    bigo_password = account['password']
    bigo_country = account['country']
    bigo_live = account['live_id']
    print(f"Handling account with live_id: {bigo_live}")

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
            handle_account(driver, account)

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
            handle_account(driver, account)

        try:
            login_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "head-right__login__btn"))
            )
            login_button.click()
            delay()
        except:
            driver.quit()
            handle_account(driver, account)

        try:
            sign_up_link = WebDriverWait(driver, 70).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up now')]"))
            )
            sign_up_link.click()
            delay()
        except:
            driver.quit()
            handle_account(driver, account)

        try:
            login_tab_button = WebDriverWait(driver, 90).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "tab-login-sign__item"))
            )
            login_tab_button.click()
            delay()
        except:
            driver.quit()
            handle_account(driver, account)

        try:
            country_select_component = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".CountrySelect-Component"))
            )
            country_select_component.click()
            delay()
        except:
            driver.quit()
            handle_account(driver, account)

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

        time.sleep(1)
        print("login")
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
            post_comment(driver, bigo_comments)
        except Exception as e:
            post_comment(driver, bigo_comments)
            print("end write comment 2")
            print(f"Error in sending text to textarea: {str(e)}")

    except Exception as e:
        print(f"Error during execution 101: {str(e)}")

    # Final actions or cleanup
    input("Press any key to close the browser...")
    # driver.quit()


UPDATE_INTERVAL = 60  # Update every 60 seconds (1 minute)

def periodic_update(driver):
    while True:
        updated_account = update_accounts(driver)
        print('updated_account', updated_account)
        time.sleep(UPDATE_INTERVAL)

def main():
    options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-dev-shm-usage')

    try:
        print("Init Driver")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("End Driver")
        updated_account = update_accounts(driver)
        update_comments()
        print('updated_account', updated_account)
        print('bigo_comments', bigo_comments)
        print("Initial bigo_live:", bigo_live)
        handle_account(driver, updated_account)
        update_thread = threading.Thread(target=periodic_update, args=(driver,), daemon=True)
        update_thread.start()
    except Exception as e:
        print(f"Error during execution 101: {str(e)}")


if __name__ == "__main__":
    main()
