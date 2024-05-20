import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_driver():
    options = Options()
    options.headless = True  # Run in headless mode
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

urls = ["https://www.google.com" for _ in range(10)]  # List of URLs or tasks

# Number of concurrent workers
num_workers = 10  # Adjust based on your system capabilities

with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    executor.map(run_task, urls)
