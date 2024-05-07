import time
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


def delay(delay=0.2):
    time.sleep(delay)


# options = Options()
# options.add_argument("--headless")
# options.add_argument('--no-sandbox')  # Bypass OS security model
# options.add_argument('--disable-gpu')  # GPU hardware acceleration isn't necessary
# options.add_argument('--window-size=1920x1080')  # Define the window size
# options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
# driver = webdriver.Chrome(options=options)

# Setup Chrome and WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
driver.get("https://m.hzmk.site/")
WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')
# Handling various elements before the slider
try:
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

    egypt_li = WebDriverWait(driver, 110).until(
        EC.visibility_of_element_located((By.XPATH, "//li[contains(span/text(), 'Egypt')]"))
    )
    egypt_li.click()
    delay()

    phone_input = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".LoginForm-Component .phone-number-box input"))
    )
    phone_input.send_keys("1016220238")
    delay()

    password_input = WebDriverWait(driver, 130).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".LoginForm-Component .password-tab input"))
    )
    password_input.send_keys("m3290900a")
    delay()

    print("Sleep")
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
    print("Text of slider:", slider_handle.text)
    delay(0.5)

    captcha_text_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textelediv"))
    )
    captcha_text = captcha_text_element.text
    print("Captcha Text:", captcha_text)

    # Make movement relative and ensure not to exceed track limits
    move_step = track_width // 20  # Using smaller, more precise steps
    for i in range(20):
        action.move_by_offset(move_step, 0)  # Move horizontally without vertical deviation
        action.pause(random.uniform(0.05, 0.1))
    action.release().perform()

    captcha_text_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "captcha-box-login-bigo-captcha-element-bigo-captcha-textelediv"))
    )
    captcha_text = captcha_text_element.text
    print("Captcha Text:", captcha_text)

    print("login")
    time.sleep(3)
    submit_login = WebDriverWait(driver, 150).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-sumbit")))
    submit_login.click()
    print("end login")

    print("open live")
    time.sleep(3)
    driver.get("https://m.hzmk.site/901584560")
    print("end open live")
    print("write comment")
    time.sleep(3)
    try:
        textarea = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea"))
        )
        textarea.send_keys("Hallo da bin ich vieder")
        textarea.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Error in sending text to textarea: {str(e)}")

    print("end write comment")
except Exception as e:
    print(f"Error during execution: {str(e)}")

# Final actions or cleanup
input("Press any key to close the browser...")
driver.quit()
