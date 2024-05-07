import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome and WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
driver.get("https://m.hzmk.site/")

privacy_confirm_element = WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.ID, "privacy-confirm-ele"))
)
privacy_confirm_element.click()

close_button = WebDriverWait(driver, 50).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "close"))
)
close_button.click()

login_button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "head-right__login__btn"))
)
login_button.click()

sign_up_link = WebDriverWait(driver, 70).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up now')]"))
)
sign_up_link.click()

login_tab_button = WebDriverWait(driver, 90).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "tab-login-sign__item"))
)
login_tab_button.click()

country_select_component = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".CountrySelect-Component"))
)
country_select_component.click()

egypt_li = WebDriverWait(driver, 110).until(
    EC.visibility_of_element_located((By.XPATH, "//li[contains(span/text(), 'Egypt')]"))
)
egypt_li.click()

phone_input = WebDriverWait(driver, 120).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".LoginForm-Component .phone-number-box input"))
)
phone_input.send_keys("01553990162")

password_input = WebDriverWait(driver, 130).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".LoginForm-Component .password-tab input"))
)
password_input.send_keys("Admin2020")

print("Sleep")
time.sleep(15)
print("Wake")

# Slider captcha handling
slider = WebDriverWait(driver, 140).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".slider-button"))  # Update the selector based on actual HTML
)
track = WebDriverWait(driver, 140).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".slider-track"))  # Update if necessary
)

# Perform the drag and drop action
action = ActionChains(driver)
track_width = track.size['width']
slider_width = slider.size['width']
movement_length = track_width - slider_width  # Adjust based on the end buffer if needed
action.click_and_hold(slider).move_by_offset(movement_length, 0).release().perform()

# Wait a little for any post-move verification that might occur
print("Finish")
input("Press any key to close the browser...")
driver.quit()
