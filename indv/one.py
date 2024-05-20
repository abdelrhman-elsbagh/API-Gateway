import os
import time
from multiprocessing import Pool, Lock
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

bigo_live = '1003946142'

bgb_account = {
        'bigo_phone': "1069339515",
        'bigo_password': "m3290900a",
        'bigo_country': 'Egypt',
    }

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

def handle_account(account):
    bigo_phone = account['bigo_phone']
    bigo_password = account['bigo_password']
    bigo_country = account['bigo_country']

    print(f"account {bigo_phone} , country {bigo_country} , password {bigo_password}")

    # caps = DesiredCapabilities.CHROME
    # caps['pageLoadStrategy'] = "eager"

    print("Init Options")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # GPU hardware acceleration isn't necessary
    options.add_argument('--window-size=1920x1080')  # Define the window size
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
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

    try:
        print("IPPPPP")
        driver.get(TARGET)
        with open("one.html", "w") as f:
            f.write(driver.page_source)
    except Exception as e:
        print("IPPP error target", e)

    driver.get("https://m.hzmk.site/")
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')
    try:
        print("start Script")
        privacy_confirm_element = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.ID, "privacy-confirm-ele"))
        )
        privacy_confirm_element.click()
        delay()

        close_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "close"))
        )
        close_button.click()
        delay()

        login_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "head-right__login__btn"))
        )
        login_button.click()
        delay()

        sign_up_link = WebDriverWait(driver, 70).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up now')]"))
        )
        sign_up_link.click()
        delay()

        login_tab_button = WebDriverWait(driver, 90).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "tab-login-sign__item"))
        )
        login_tab_button.click()
        delay()

        country_select_component = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".CountrySelect-Component"))
        )
        country_select_component.click()
        delay()

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

        print(f"Sleep {bigo_phone}")
        time.sleep(6)
        print("Wake")

        slider_track = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textele"))
        )
        track_width = slider_track.size['width']

        slider_handle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-sliderele"))
        )
        action = ActionChains(driver)
        action.click_and_hold(slider_handle)

        print("captcha is ready")
        print(f"Text of slider: {bigo_phone}", slider_handle.text)
        delay(0.5)

        captcha_text_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textelediv"))
        )
        captcha_text = captcha_text_element.text
        print(f"Captcha Text: {bigo_phone}", captcha_text)

        # Make movement relative and ensure not to exceed track limits
        move_step = track_width // 20  # Using smaller, more precise steps
        for i in range(25):
            action.move_by_offset(move_step, 0)  # Move horizontally without vertical deviation
            action.pause(random.uniform(0.05, 0.1))
        action.release().perform()

        captcha_text_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textelediv"))
        )
        captcha_text = captcha_text_element.text
        print("Captcha Text:", captcha_text)

        success_captcha = 'Verification successful'
        if success_captcha not in captcha_text:
            handle_account(account)

        print("login")
        time.sleep(5)
        submit_login = WebDriverWait(driver, 150).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-sumbit")))
        submit_login.click()
        print(f"end login {bigo_phone}")

        print("open live")
        time.sleep(5)
        driver.get("https://m.hzmk.site/" + bigo_live)
        print("end open live")
        print(f"write comment {bigo_phone}")
        time.sleep(3)
        try:
            textarea = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea"))
            )
            textarea.send_keys("  ****Hallo da bin ich vieder ****" + bigo_phone)
            time.sleep(2)
            textarea.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Error in sending text to textarea: {str(e)}")
            handle_account(account)

        print("end write comment")
    except Exception as e:
        print(f"Error during execution: {str(e)}")

    input("Press any key to close the browser...")
    driver.quit()


def main():
    num_cores = os.cpu_count()  # Get the number of cores available
    print(f"Running on {num_cores} cores")
    handle_account(bgb_account)


if __name__ == "__main__":
    main()
