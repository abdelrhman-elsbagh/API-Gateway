import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open the URL
driver.get("https://egy.almaviva-visa.it/appointment")

WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')

WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
                    )

email_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
)
email_input.send_keys("abdelrahman.tarek.elsbagh@gmail.com")
time.sleep(1)
password_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
)
password_input.send_keys("Admin@2030")
password_input.send_keys(Keys.ENTER)

time.sleep(2)
driver.get("https://egy.almaviva-visa.it/appointment")
time.sleep(6)

input("press key to book")

WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mat-mdc-option')))

option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Cairo')]"))
)
option.click()


option2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-mdc-option"))
)
option2.click()


option2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Employment Visa C')]"))
)
option2.click()

checkbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox'][id='mat-mdc-checkbox-1-input']"))
)
checkbox.click()

date_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[formcontrolname='tripDate']"))
)
driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
date_input.send_keys("10/10/2025")

destination_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[formcontrolname='tripDestination']"))
)
destination_input.send_keys("Roma")


button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".visasys-button.w-72.mt-6"))
)

while True:
    button.click()
    time.sleep(0.2)

input("Press any key to quit")
driver.quit()
