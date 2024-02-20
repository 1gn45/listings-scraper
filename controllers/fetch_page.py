import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc


def fetch_page(url: str, driver: WebDriver | None = None) -> WebDriver:
    chrome_options = Options()

    if not driver:
        print("creating driver")
        driver = uc.Chrome(use_subprocess=False, options=chrome_options)

    print("fetching page")
    print(url)
    driver.get(url)
    print("page fetched")

    return driver
