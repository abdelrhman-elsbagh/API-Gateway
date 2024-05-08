# import urllib.request
# import random
# username = 'abdel9'
# password = 'Admin_2050Pass'
# entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
# (username, password))
# query = urllib.request.ProxyHandler({
# 'http': entry,
# 'https': entry,
# })
# execute = urllib.request.build_opener(query)
# print(execute.open('https://ip.oxylabs.io/location').read())

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def init_driver():
    options = webdriver.ChromeOptions()
    proxy = "customer-abdel9:Admin_2050Pass@pr.oxylabs.io:7777"
    options.add_argument(f'--proxy-server=http://{proxy}')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--verbose")
    options.add_argument("--log-path=chromedriver.log")

    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)