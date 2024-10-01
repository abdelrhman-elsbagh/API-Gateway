import json
import os
import re
import signal
import sys
import threading
import time
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
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

from webdriver_manager.firefox import GeckoDriverManager

API_URL = "https://ske.live/api/live-data"
BASE_URL = "https://ske.live/api"
API_Comments_URL = "https://ske.live/api/comments"

CHECK_INTERVAL = 10

BASE_LIVE_URL = "https://www.bigo.tv/"

global bigo_comments, bigo_live, LOGIN_SUCCESS, account, main_phone
bigo_live = ""
bigo_comments = []

LOGIN_SUCCESS = False

UPDATE_INTERVAL = 1  # Update every 60 seconds
UPDATE_20_INTERVAL = 6  # Update every 20 seconds

json_file_path = os.path.join(os.getcwd(), 'account_data.json')


def get_account():
    current_account = None
    global main_phone, account
    # Check if the 'account_data.json' file exists
    if not os.path.exists('account_data.json'):
        # Step 1: Call the endpoint
        url = f"{BASE_URL}/available-account"
        response = requests.get(url, timeout=30)

        # Step 2: Check if the response is successful
        print("Fetch Account is ", response.json())
        if response.status_code == 200:
            current_account = response.json()
            print("get_account phone", current_account.get('main_phone'))
            main_phone = current_account.get('main_phone')
            account = current_account.get('account', {})
            # Step 3: Write the data to a JSON file
            with open('account_data.json', 'w') as file:
                json.dump(current_account, file, indent=4)
            print("Account data saved to 'account_data.json'")
            return current_account
        else:
            print(f"Failed to retrieve account data. Status code: {response.status_code}")
    else:
        print("'account_data.json' already exists, skipping the request.")

    return current_account


# Load the login data from JSON file if it exists
def load_login_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    return {}


# Save the login data to a JSON file
def save_login_data(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)


# Load cookies from a JSON file
def load_cookies(driver, cookies_file):
    print("cookies_file ", str(cookies_file))
    global LOGIN_SUCCESS
    if os.path.exists(cookies_file):
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded successfully.")
        LOGIN_SUCCESS = True
        # print("Loaded Cookies:", driver.get_cookies())
        update_in_use_status(main_phone, True)
    else:
        print("No cookies file found. Login required.")


# Save cookies to a JSON file
def save_cookies(driver, cookies_file):
    print("driver.get_cookies", driver.get_cookies())
    if not os.path.exists(cookies_file):
        with open(cookies_file, 'w') as f:
            json.dump(driver.get_cookies(), f)
        print("Cookies saved successfully.")
    else:
        print(f"The file '{cookies_file}' already exists. Cookies were not saved.")


# Load existing login data or initialize with default values
login_data = load_login_data(json_file_path)
main_phone = login_data.get('main_phone', '')
account = login_data.get('account', {})

if main_phone == '' or main_phone is None:
    main_phone = get_account().get('main_phone')
    # account = get_account().get('account')

folder_path = os.path.join(os.getcwd(), 'login_cookies')
# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)
cookies_file_path = os.path.join(folder_path, f'{main_phone}.json')

print("Main Phone:", main_phone)
print("Account Details:", account)


def fetch_config():
    global BASE_LIVE_URL
    response = requests.get(f"{BASE_URL}/config", timeout=30)
    if response.status_code == 200:
        BASE_LIVE_URL = response.json()['base_url']
    else:
        print(f"Failed to fetch accounts: {response.status_code}")
        BASE_LIVE_URL = "https://www.bigo.tv/"


def get_current_path(driver):
    current_url = driver.current_url
    parsed_url = urlparse(current_url)
    path = parsed_url.path
    return path


def wait_for_elementv2(driver, locator, timeout=10):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def post_comment(driver, comments):
    global main_phone
    try:
        time.sleep(2)
        textarea_locator = (By.CSS_SELECTOR, "textarea")

        # Wait for the textarea to be present and visible
        textarea = wait_for_element(driver, textarea_locator)

        print("write post_comment")
        time.sleep(1)

        if comments is None:
            comments = update_comments()

        if len(comments) < 1:
            comments = update_comments()

        random_comment = random.choice(comments)
        textarea.send_keys(str(random_comment))
        time.sleep(2)
        print("Current Comment: ", random_comment)
        textarea.send_keys(Keys.ENTER)

        increment_comment_num(main_phone)

        print("end write comment")
    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_comments(api_url):
    response = requests.get(api_url, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch accounts: {response.status_code}")
        return []


import requests


def update_in_use_status(phone_number, in_use):
    print("update_in_use_status", phone_number, in_use)
    # Define the API endpoint
    endpoint = f"{BASE_URL}/update-in-use"

    # Prepare the data payload
    payload = {
        "phone": phone_number,
        "in_use": in_use
    }

    try:
        # Send a POST request to the API
        response = requests.post(endpoint, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Successfully updated 'in_use' status for phone {phone_number}.")
            return response.json()
        else:
            print(f"Failed to update 'in_use' status. Status code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def get_live_by_phone(phone):
    try:
        response = requests.get(f"{BASE_URL}/live-phone", params={'phone': phone}, timeout=30)
        if response.status_code == 200:
            if response.text:
                return response.json()
            else:
                return {'success': False, 'message': 'Empty response'}
        else:
            return {'success': False, 'message': f'Request failed with status code {response.status_code}'}
    except Exception as e:
        print("get_live_by_phone exception")
        return {'success': False, 'message': str(e)}


def post_comment_if_live_id_matches(driver, live_id, comment):
    """
    Check the current tab's URL, and if it matches the given live_id, post the comment.
    """
    current_url = driver.current_url
    if live_id in current_url:  # Check if live_id is part of the URL
        print(f"Found live_id {live_id} in URL, posting comment...")
        textarea_locator = (By.CSS_SELECTOR, "textarea")
        try:
            # Wait for the textarea to be present and visible
            textarea = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(textarea_locator))
            textarea.send_keys(comment)
            time.sleep(1)
            textarea.send_keys(Keys.ENTER)
            print(f"Comment '{comment}' posted successfully.")
            delay(5)
            increment_comment_num(main_phone)
        except TimeoutException:
            print(f"Could not post comment for {live_id}. Textarea not found.")
    else:
        print(f"live_id {live_id} not found in current URL. Skipping.")


def manage_tabs_and_post_comments(driver, live_ids, comments):
    """
    Iterate over all tabs, check if the live_id exists in the current live_ids list.
    If it exists, write the comment; otherwise, close the tab.
    """
    original_tab = driver.window_handles[0]  # Keep the first/origin tab open (https://www.bigo.tv/)

    # Iterate over each tab
    for i, handle in enumerate(driver.window_handles):
        driver.switch_to.window(handle)
        current_url = driver.current_url

        if "bigo.tv" in current_url:
            if current_url == "https://www.bigo.tv/":
                continue  # Skip the origin tab

            # Extract live_id from the URL (if present)
            current_live_id = current_url.split('/')[-1]

            if current_live_id in live_ids:
                # Post a comment if the live_id exists in the current list
                if i < len(comments):  # Ensure there's a comment for this live_id
                    post_comment_if_live_id_matches(driver, current_live_id, comments[i])
            else:
                # If live_id is not in the current list, close the tab
                print(f"Closing tab for live_id {current_live_id} as it's no longer in the live_id list.")
                driver.close()

    # After managing all tabs, switch back to the original tab
    driver.switch_to.window(original_tab)


def close_all_tabs_except_origin(driver, origin_url="https://www.bigo.tv/"):
    """
    Closes all tabs except for the origin tab (https://www.bigo.tv/).
    """
    original_tab = driver.window_handles[0]  # Keep the first/origin tab open

    # Iterate over each tab except the first one
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        current_url = driver.current_url

        if current_url != origin_url:
            print(f"Closing tab with URL: {current_url}")
            driver.close()

    # Switch back to the original tab
    driver.switch_to.window(original_tab)
    driver.get(origin_url)


def close_all_tabs_except_one(driver):
    """
    Closes all tabs except one, keeping the browser open.
    If the remaining tab's URL is not 'https://www.bigo.tv/', redirect it to that page.
    """
    original_tab = driver.window_handles[0]  # Get the first open tab

    # Close all other tabs except the first one
    for handle in driver.window_handles[1:]:
        driver.switch_to.window(handle)
        print(f"Closing tab with URL: {driver.current_url}")
        driver.close()

    # Switch back to the original tab
    driver.switch_to.window(original_tab)
    current_url = driver.current_url

    # If the list of live_ids is empty and the current URL is not 'https://www.bigo.tv/', redirect
    if current_url != "https://www.bigo.tv/":
        print("Redirecting the remaining tab to https://www.bigo.tv/")
        driver.get("https://www.bigo.tv/")

def manage_tabs(driver, new_live_ids):
    """
    Manage existing tabs. Use the first tab for the first live_id, open new tabs for remaining live_ids,
    and close tabs for live_ids no longer in the list.
    Implement retry mechanism to handle network issues.
    """
    open_live_ids = []
    origin_handle = driver.window_handles[0]  # Save the first tab's handle

    # Retry mechanism for network issues
    def load_url_with_retry(url, retries=3, delay=5):
        attempt = 0
        while attempt < retries:
            try:
                driver.get(url)
                print(f"Successfully loaded {url}")
                return True
            except WebDriverException as e:
                print(f"Error loading {url}: {e}")
                if 'ERR_CONNECTION_RESET' in str(e):
                    attempt += 1
                    print(f"Retrying ({attempt}/{retries}) in {delay} seconds...")
                    time.sleep(delay)  # Wait before retrying
                else:
                    raise  # If the error is not network-related, raise it
        return False  # If all retries fail

    # Use the first live_id for the original tab
    first_live_id = new_live_ids[0]  # First live_id
    driver.switch_to.window(origin_handle)

    # Get the current URL of the original tab
    current_url = driver.current_url

    # Only load the live_id if it's not already in the current tab
    if not current_url.endswith(f"/{first_live_id}"):
        success = load_url_with_retry(f"https://www.bigo.tv/{first_live_id}")
        if not success:
            print(f"Failed to load {first_live_id} after multiple attempts, skipping.")
        else:
            open_live_ids.append(first_live_id)
    else:
        print(f"Original tab already points to live_id {first_live_id}, skipping redirect.")
        open_live_ids.append(first_live_id)

    # Manage existing tabs and open new ones for the remaining live_ids
    for handle in driver.window_handles[1:]:  # Skip the first tab
        driver.switch_to.window(handle)
        current_url = driver.current_url
        time.sleep(5)  # Add a delay between tab switches

        # Extract live_id from URL
        current_live_id = current_url.split('/')[-1]

        if current_live_id in new_live_ids:
            open_live_ids.append(current_live_id)  # Keep tabs that are still relevant
        else:
            print(f"Closing tab for live_id {current_live_id}")
            driver.close()  # Close tabs that no longer have relevant live_ids

    # Open new tabs for live_ids that aren't already open
    for live_id in new_live_ids[1:]:
        if live_id not in open_live_ids:
            print(f"Opening new tab for live_id {live_id}")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            success = load_url_with_retry(f"https://www.bigo.tv/{live_id}")

            if not success:
                print(f"Failed to load {live_id} after multiple attempts, skipping.")
            else:
                open_live_ids.append(live_id)

    # Switch back to the first tab after managing all tabs
    driver.switch_to.window(origin_handle)

def remove_non_bmp_characters(text):
    """
    Removes any characters that are outside the Basic Multilingual Plane (BMP).
    """
    # Use a regex to remove characters outside the BMP range
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

# I use it if there is cookie file and loaded & login success
def update_accounts(driver):
    try:
        global LOGIN_SUCCESS, UPDATE_INTERVAL, bigo_live, bigo_comments, account
        print("update_accounts function")
        print("LOGIN_SUCCESS:", LOGIN_SUCCESS)

        # Fetch data using your get_live_by_phone function
        data = get_live_by_phone(main_phone)
        print("get the account now", data)
        bigo_comments = update_comments()
        print("bigo_comments", bigo_comments)

        try:
            # Update interval for comments
            UPDATE_INTERVAL = data['comment_time']
        except Exception as e:
            print(e)

        # Handle case where phone data is not found or 'account' is missing
        if 'success' in data and not data['success']:
            print(f"Phone {main_phone} Not Found")
            print(f"Local Account is {account}")
            bigo_live = []  # Reset bigo_live to an empty list
            account["live_id"] = []

            # Close all tabs except one (keeping browser open)
            close_all_tabs_except_one(driver)

            return account

        # Check if 'account' and 'live_id' exist in the response data
        if 'account' in data and 'live_id' in data['account']:
            # Ensure live_id is a list
            new_live_ids = data['account']['live_id'] if isinstance(data['account']['live_id'], list) else [
                data['account']['live_id']]
        else:
            print("No live_id found in data, closing all tabs except one.")
            bigo_live = []  # Reset the live_id list

            # Close all tabs except one (keeping browser open)
            close_all_tabs_except_one(driver)

            return account

        # If no live_id is being tracked currently
        if not new_live_ids:
            print("No live_id to track, closing all tabs except one.")
            bigo_live = []  # Clear out the current live_id list

            # Close all tabs except one (keeping browser open)
            close_all_tabs_except_one(driver)

            return account

        # Manage tabs for the new live_ids
        manage_tabs(driver, new_live_ids)

        # Post comments in the appropriate tabs
        if LOGIN_SUCCESS and bigo_live and bigo_comments:
            for i, handle in enumerate(driver.window_handles):  # Iterate over open tabs
                driver.switch_to.window(handle)
                current_url = driver.current_url
                time.sleep(5)  # Add a delay when switching between tabs

                # Extract live_id from the current tab's URL
                current_live_id = current_url.split('/')[-1]

                # check if the live-stream is off will stop this live
                try:
                    print(f"check live stream is active or no {current_live_id}")
                    element = driver.find_element(By.CLASS_NAME, 'live--off-title')
                    print("Class 'live--off-title' exists on the page.")
                    stop_live(current_live_id)
                except Exception as strm_exp:
                    print("Class 'live--off-title' does not exist on the page.")

                if current_live_id in bigo_live:
                    # Post the comment corresponding to the current live_id
                    random_comment = random.choice(bigo_comments)
                    post_comment_if_live_id_matches(driver, current_live_id, random_comment)

        # Update global live_id tracker
        bigo_live = new_live_ids  # Ensure it's now a list of live_ids
        print(f"Tracking the following live_ids: {bigo_live}")

        # Update the account information
        account = {
            'phone': data['account']['phone'],
            'password': data['account']['password'],
            'country': data['account']['country'],
            'live_id': new_live_ids,  # Ensure it's now a list of live_ids
            'comment_time': data['comment_time'],
        }

        # Update interval for comments
        UPDATE_INTERVAL = data['comment_time']

        print("Account has been updated:", account)

        return account
    except Exception as e:
        print('update_accounts exception ' + str(e))
        time.sleep(30)
        update_accounts(driver)


def update_comments():
    global bigo_comments
    bigo_comments = []
    comments_data = fetch_comments(API_Comments_URL)
    for comment in comments_data:
        bigo_comments.append(comment['comment'])

    bigo_comments = [remove_non_bmp_characters(comment) for comment in bigo_comments]
    return bigo_comments


def delay(delay=0.2):
    time.sleep(delay)


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
        delay(0.1)


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
                    handle_slider_verification(driver, 1)
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
                    handle_slider_verification(driver, 1)
        except Exception as e:
            print(f"Error during slider verification attempt {retry_count + 1}: {e}")
            retry_count += 1
            if retry_count >= max_retries:
                print("Reached maximum retries due to exceptions. Exiting.")
                handle_slider_verification(driver, 1)
                return False
    print("Captcha verification process completed with failures.")
    driver.quit()
    main()


def handle_account(driver, account):
    print("handle_account started")
    global bigo_live, LOGIN_SUCCESS

    bigo_phone = account['phone']
    bigo_password = account['password']
    bigo_country = account['country']
    bigo_live = account['live_id']
    print(f"Handling account with live_id: {bigo_live}")

    if bigo_live != "":
        print(f"Init Open Live {bigo_live}")
        driver.get(f"https://www.bigo.tv/{bigo_live}")
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState;') == 'complete')
        print(f"End Openninig {bigo_live}")
    try:
        try:
            print("Accept privacy")
            privacy_confirm_element = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.ID, "privacy-confirm-ele"))
            )
            privacy_confirm_element.click()
            delay()
        except Exception as e:
            print("Accept privacy error", e)
            handle_account(driver, account)

        print('Middle')

        try:
            close_button = WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "close"))
            )
            close_button.click()
            delay()
            print("End privacy")
        except Exception as e:
            print("close_button error", e)
            # handle_account(driver, account)

        try:
            login_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "head-right__login__btn"))
            )
            login_button.click()
            delay()
        except Exception as e:
            print("login_button error", e)
            handle_account(driver, account)

        try:
            sign_up_link = WebDriverWait(driver, 70).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up now')]"))
            )
            sign_up_link.click()
            delay()
        except Exception as e:
            print("sign_up_link error", e)
            handle_account(driver, account)

        try:
            login_tab_button = WebDriverWait(driver, 90).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "tab-login-sign__item"))
            )
            login_tab_button.click()
            delay()
        except Exception as e:
            print("login_tab_button error", e)
            handle_account(driver, account)

        try:
            country_select_component = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".CountrySelect-Component"))
            )
            country_select_component.click()
            delay()
        except:
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
        time.sleep(5)
        print("Wake")

        ## Handle Slider
        handle_slider_verification(driver)

        time.sleep(1)
        print("login")
        submit_login = WebDriverWait(driver, 150).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-sumbit")))
        submit_login.click()
        print("end login")

        # Save cookies after successful login

        # try:
        #     update_in_use_status(main_phone, True)
        # except Exception as update_in_use_status_err:
        #     print("update_in_use_status_err", update_in_use_status_err)

        print("Save Cookie Number ", main_phone)
        save_cookies(driver, cookies_file_path)

        try:
            time.sleep(2)
            textarea_present = EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
            WebDriverWait(driver, 10).until(textarea_present)
            textarea_locator = (By.CSS_SELECTOR, "textarea")
            wait_for_element(driver, textarea_locator)
            print("open live")
        except Exception as e:
            print("open live 2")
            print(f"Error in located : {str(e)}")
            LOGIN_SUCCESS = True
            return True

        if bigo_live != "":
            print("write comment main")
            try:
                global bigo_comments
                print("bigo_comments-handle_account", bigo_comments)
                bigo_comments = update_comments()
                post_comment(driver, bigo_comments)
            except Exception as e:
                print("end write comment 2")
                print(f"Error in sending text to textarea: {str(e)}")

    except Exception as e:
        print(f"Error during execution 101: {str(e)}")
        print("re run handle_account() 101")
        handle_account(driver, account)

    LOGIN_SUCCESS = True
    update_accounts(driver)


def increment_comment_num(phone_number):
    # Define the URL for the API endpoint
    url = f"{BASE_URL}/increment-comment-num"

    # Define the data to be sent in the POST request
    data = {
        'phone': phone_number
    }
    try:
        # Send a POST request to the API
        response = requests.post(url, data=data, timeout=30)
    except requests.RequestException as e:
        # Print an error message if there was an exception during the request
        print(f"An error occurred: {e}")


def increment_run_time(phone_number):
    # Define the URL for the API endpoint
    url = f"{BASE_URL}/increment-run-time"

    # Define the data to be sent in the POST request
    data = {
        'phone': phone_number
    }
    try:
        # Send a POST request to the API
        response = requests.post(url, data=data, timeout=30)
    except requests.RequestException as e:
        # Print an error message if there was an exception during the request
        print(f"An error occurred: {e}")


def stop_live(live_id):
    print(f"we have entered to stop_live {live_id}")
    # Define the URL for the API endpoint
    url = f"{BASE_URL}/live/stop"

    # Define the data to be sent in the POST request
    data = {
        'live_id': live_id
    }
    try:
        # Send a POST request to the API
        response = requests.post(url, data=data, timeout=30)
        print(response)
    except requests.RequestException as e:
        # Print an error message if there was an exception during the request
        print(f"An error occurred: {e}")

def periodic_update(driver):
    global UPDATE_INTERVAL
    print("UPDATE_INTERVAL", UPDATE_INTERVAL)
    while True:
        updated_account = update_accounts(driver)
        print('periodic_update function', updated_account)
        time.sleep(UPDATE_INTERVAL * 60)


def periodic_put_comment(driver, bigo_comments):
    while True:
        updated_comment = post_comment(driver, bigo_comments)
        print('updated_comment', updated_comment)
        # print('UPDATE_20_INTERVAL', UPDATE_20_INTERVAL)
        # time.sleep(UPDATE_20_INTERVAL * 60)


def sigterm_handler(signum, frame):
    print("Press Enter to close the browser...")
    sys.exit(0)  # Exit gracefully


def main():
    global bigo_comments, main_phone, account
    increment_run_time(main_phone)
    get_account()

    # proxy = "192.168.1.6:30002"
    sys.setrecursionlimit(100000)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument(f'--proxy-server={proxy}')

    port = 30002
    # options = webdriver.FirefoxOptions()
    # options.set_preference('network.proxy.type', 1)
    # options.set_preference('network.proxy.http', '192.168.1.6')
    # options.set_preference('network.proxy.http_port', port)
    # options.set_preference('network.proxy.ssl', '192.168.1.6')
    # options.set_preference('network.proxy.ssl_port', port)
    # options.set_preference('network.proxy.socks', '192.168.1.6')
    # options.set_preference('network.proxy.socks_port', port)
    # options.set_preference('network.proxy.ftp', '192.168.1.6')
    # options.set_preference('network.proxy.ftp_port', port)
    # # options.set_preference('network.proxy.no_proxies_on', '')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')

    # try:
    print("Init Driver")
    # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("End Driver")
    driver.get("https://www.bigo.tv/")
    load_cookies(driver, cookies_file_path)

    driver.refresh()

    # if not driver.get_cookie('user_name'):
    if not os.path.exists(cookies_file_path):
        print("sessionid not found", cookies_file_path)
        updated_account = update_accounts(driver)
        bigo_comments = update_comments()
        print('updated_account_co', updated_account)
        print('bigo_comments_co', bigo_comments)
        print("Initial bigo_live_co:", bigo_live)
        handle_account(driver, updated_account)
    else:
        print("Session restored from cookies.")
        update_accounts(driver)

    print("Abdel Login Status", LOGIN_SUCCESS)
    update_thread = threading.Thread(target=periodic_update, args=(driver,), daemon=True)
    update_thread.start()

    # except Exception as e:
    #     print(f"Error during execution 109: {str(e)}")
    #     print("re run main()")
    #     time.sleep(30)
    #     main()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    main()
    try:
        signal.pause()
    except Exception as e:
        # update_in_use_status(main_phone, False)
        input("press any key to quit")
        exit(1)
