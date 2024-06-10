from selenium import webdriver

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open multiple tabs (example)
urls = ["https://www.example1.com", "https://www.google.com", "https://www.example3.com"]
for url in urls:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)

# Function to find and switch to the tab with a specific URL fragment
def switch_to_tab_with_url_fragment(driver, fragment):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if fragment in driver.current_url:
            print(f"Switched to tab with URL containing '{fragment}': {driver.current_url}")
            return handle
    print(f"No tab found with URL containing '{fragment}'")
    return None

# Function to find and close the tab with a specific URL fragment
def close_tab_with_url_fragment(driver, fragment):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if fragment in driver.current_url:
            print(f"Closing tab with URL containing '{fragment}': {driver.current_url}")
            driver.close()
            # After closing a tab, switch back to the first tab to continue
            driver.switch_to.window(driver.window_handles[0])
            return True
    print(f"No tab found with URL containing '{fragment}'")
    return False

# Example: Switch to the tab containing "google.com"
switch_to_tab_with_url_fragment(driver, "google.com")
f
# Example: Close the tab containing "google.com"
close_tab_with_url_fragment(driver, "google.com")

# Optionally, do more operations...

# Clean up: Close the driver
input("please click any key to quick ...")
driver.quit()
