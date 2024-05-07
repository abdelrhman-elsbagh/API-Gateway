import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    # Setup Chrome and WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState;') == 'complete')

    try:
        # Click the login button to open the login form
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "login-button-class-name"))  # Adjust class name as needed
        )
        login_button.click()

        # Enter username
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username-input-id"))  # Adjust ID as needed
        )
        username_input.send_keys(username)

        # Enter password
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password-input-id"))  # Adjust ID as needed
        )
        password_input.send_keys(password)

        # Submit login form
        submit_button = driver.find_element(By.ID, "submit-button-id")  # Adjust ID as needed
        submit_button.click()

        # Check for login success
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "post-login-element-id"))
            # Adjust ID to an element that indicates successful login
        )
        print("Login successful")
        return True
    except TimeoutException:
        print("Login failed")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def main():
    driver = setup_driver()
    successful = login(driver, "https://m.hzmk.site/", "111", "111")
    if successful:
        print("Proceeding with post-login actions...")
    else:
        print("Check login credentials or site status.")

    # Cleanup
    driver.quit()


if __name__ == "__main__":
    main()
