from selenium import __version__ as seleniumversion
from seleniumwire import __version__ as seleniumwireversion
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
# A package to have a chromedriver always up-to-date.
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager import __version__ as webdriver_manager_version
USERNAME = "abdel9"
PASSWORD = "Admin_2050Pass"
TARGET = "https://ip.oxylabs.io"
ENDPOINT = "pr.oxylabs.io:7777"
import sys
import time
def is_selenium_version_above_4_10() -> bool:
    parts = seleniumversion.split(".")
    return len(parts) >= 2 and (
    (int(parts[0]) == 4 and int(parts[1]) >= 10)
    or int(parts[0]) > 4
    )
def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
    "proxy": {
    "http": f"https://{user}:{password}@{endpoint}",
    "https": f"https://{user}:{password}@{endpoint}",
    }
    }
    return wire_options
def execute_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    proxies = chrome_proxy(USERNAME, PASSWORD, ENDPOINT)
    if is_selenium_version_above_4_10():
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(
        service=service,
        options=options,
        seleniumwire_options=proxies,
        )
    else:
        driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options,
        seleniumwire_options=proxies,
        )
    try:
        driver.get(TARGET)
        with open("res.html", "w") as f:
            f.write(driver.page_source)
            return f'\nBody: {driver.page_source}'
    finally:
        driver.quit()

if __name__ == '__main__':
    print(execute_driver())