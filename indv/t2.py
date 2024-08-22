from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure proxy settings
proxy = "192.168.1.4:30000"

options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server={proxy}')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://m.hzmk.site/")
    print("Successfully opened the website with the proxy")

    input("Press any key to quit")
    driver.quit()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()