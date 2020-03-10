from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import os
import time


class Driver:
    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--lang=ru')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920x1080")
       #chrome_driver = os.getcwd() + "/chromedriver"
        driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        return driver
