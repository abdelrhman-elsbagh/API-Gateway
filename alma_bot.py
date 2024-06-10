import time
from datetime import datetime
from threading import Thread
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

emails = [
    "ali198511110@gmail.com",
    # "a.li198511110@gmail.com",
    # "al.i198511110@gmail.com",
    # "ali.198511110@gmail.com",
    # "ali1.98511110@gmail.com",
    # "ali19.8511110@gmail.com",
    # "ali198.511110@gmail.com",
    # "ali1985.11110@gmail.com",
    # "ali19851.1110@gmail.com",
    # "ali198511.110@gmail.com",
    # "ali1985111.10@gmail.com",
    # "ali19851111.0@gmail.com",
    # "a.l.i198511110@gmail.com",
    # "a.li198511110@gmail.com",
    # "a.li.198511110@gmail.com",
    # "a.li1.98511110@gmail.com",
    # "a.li19.8511110@gmail.com",
    # "a.li198.511110@gmail.com",
    # "a.li1985.11110@gmail.com"
]


def login_and_wait(email):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://egyiam.almaviva-visa.it/realms/oauth2-visaSystem-realm-pkce/protocol/openid-connect/auth?response_type=code&client_id=aa-visasys-public&state=NDUtU1M5WDVpNElQUUNkemJSU3FTRl81RFdXQUJGX2ltbmM1bkJxVzhVQ2h3&redirect_uri=https%3A%2F%2Fegy.almaviva-visa.it%2F&scope=openid%20profile%20email&code_challenge=zSEUH_Eu9TQ8hWPMtyzSFZtI89JPjeLVLfxlhKMlZ2w&code_challenge_method=S256&nonce=NDUtU1M5WDVpNElQUUNkemJSU3FTRl81RFdXQUJGX2ltbmM1bkJxVzhVQ2h3")

    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')

    print("init", email)
    time.sleep(5)

    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "username"))
    )
    email_input.send_keys(email)
    time.sleep(2)
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "password"))
    )
    password_input.send_keys("Ali@1234")
    print("ready too book")
    time.sleep(3)
    password_input.send_keys(Keys.ENTER)

    time.sleep(10)
    print("goto appoiment")
    driver.get("https://egy.almaviva-visa.it/appointment")
    time.sleep(6)
    print("end appoiment")



    # Wait until exactly 9:00 AM
    target_time = datetime.now().replace(hour=3, minute=35, second=0, microsecond=0)
    while datetime.now() < target_time:
        time.sleep(1)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".visasys-button.w-72.mt-6"))
    )

    # Click the button exactly 50 times at 9:00 AM
    for _ in range(5):
        print("click")
        button.click()
        time.sleep(0.2)

    driver.quit()


threads = []
for email in emails:
    thread = Thread(target=login_and_wait, args=(email,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

input("Press any key to quit")
