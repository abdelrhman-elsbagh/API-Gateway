from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Create an instance of Options
options = Options()
options.add_argument("--start-maximized")  # Opens the browser in maximized mode
options.add_argument("--ignore-certificate-errors")  # Ignores any certificate errors

# Set additional capabilities through options if needed
# For example:
options.set_capability("browserName", "chrome")

# Create a WebDriver instance with the correct options
driver = webdriver.Remote(
    command_executor='http://192.168.1.10:4444',
    options=options
)

# Navigate to a website and print its title
driver.get("http://www.google.com")
print("Opened Google, title is:", driver.title)

# Close the browser
driver.quit()
