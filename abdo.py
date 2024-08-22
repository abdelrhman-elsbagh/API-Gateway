from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

options = webdriver.FirefoxOptions()
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)
