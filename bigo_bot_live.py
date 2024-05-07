import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920x1080")
    # options.add_argument("--disable-dev-shm-usage")
    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def click_element(wait, by_type, identifier, delay_time=0.2):
    element = wait.until(EC.element_to_be_clickable((by_type, identifier)))
    element.click()
    time.sleep(delay_time)


def send_keys_to_element(wait, by_type, identifier, keys, delay_time=0.2):
    element = wait.until(EC.visibility_of_element_located((by_type, identifier)))
    element.send_keys(keys)
    time.sleep(delay_time)


def perform_captcha_action(driver, wait, track_width):
    slider_handle = wait.until(
        EC.element_to_be_clickable((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-sliderele")))
    action = ActionChains(driver)
    action.click_and_hold(slider_handle)
    move_step = track_width // 20
    for _ in range(20):
        action.move_by_offset(move_step, 0)
        action.pause(random.uniform(0.05, 0.1))
    action.release().perform()


def main():
    driver = init_driver()
    driver.get("https://m.hzmk.site/")
    wait = WebDriverWait(driver, 10)
    try:
        click_element(wait, By.ID, "privacy-confirm-ele")
        click_element(wait, By.CLASS_NAME, "close")
        click_element(wait, By.CLASS_NAME, "head-right__login__btn")
        click_element(wait, By.XPATH, "//a[contains(text(), 'Sign up now')]")
        click_element(wait, By.CLASS_NAME, "tab-login-sign__item")
        click_element(wait, By.CSS_SELECTOR, ".CountrySelect-Component")
        click_element(wait, By.XPATH, "//li[contains(span/text(), 'Egypt')]")

        send_keys_to_element(wait, By.CSS_SELECTOR, ".LoginForm-Component .phone-number-box input", "1016220238")
        send_keys_to_element(wait, By.CSS_SELECTOR, ".LoginForm-Component .password-tab input", "m3290900a")

        slider_track = wait.until(
            EC.visibility_of_element_located((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textele")))
        perform_captcha_action(driver, wait, slider_track.size['width'])

        submit_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-sumbit")))
        submit_login.click()

        driver.get("https://m.hzmk.site/901584560")
        textarea = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea")))
        textarea.send_keys("Hallo da bin ich wieder")
        textarea.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Error during execution: {str(e)}")
    finally:
        input("Press any key to close the browser...")
        driver.quit()


if __name__ == "__main__":
    main()
