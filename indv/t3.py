from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure proxy settings
proxy = "192.168.1.3:30001"

options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server={proxy}')
options.add_argument('--disable-gpu')  # Optional: disable GPU hardware acceleration
options.add_argument('--no-sandbox')  # Optional: needed for running on some Linux environments

try:
    # Initialize the Chrome WebDriver with proxy settings
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the URL
    driver.get("https://m.hzmk.site/")
    print("Successfully opened the website with the proxy")

    # Wait for user input to keep the browser open
    input("Press any key to quit")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
