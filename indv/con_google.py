import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def run_task(url):
    driver = setup_driver()
    try:
        driver.get(url)
        print(f"Title of {url}: {driver.title}")  # Example task
        input("press any key to quick")
        driver.quit()
    finally:
        pass

run_task("https://www.google.com")
