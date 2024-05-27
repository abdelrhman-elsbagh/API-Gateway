from flask import Flask, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)


def scrape_with_selenium(url, delay=10):
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())  # Replace with the path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the page
    driver.get(url)

    # Wait for JavaScript to execute
    time.sleep(delay)

    # Get the updated page source
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    return html_content


@app.route('/scrape/<id>')
def scrape(id):
    url = f'https://m.hzmk.site/{id}'
    html_content = scrape_with_selenium(url)

    soup = BeautifulSoup(html_content, 'html.parser')
    element = soup.find(class_='live--off-title')

    if element:
        return jsonify({'value': element.get_text(strip=True)})
    else:
        return jsonify({'error': 'Element not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
