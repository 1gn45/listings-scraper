from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
from controllers.scraping.common.apply_actions_on_page import (
    apply_click_on_elements_with_innerHtml,
    apply_click_on_element_by_class,
    type_text_globally,
)
from dotenv import load_dotenv
import os

load_dotenv()

login_email = os.getenv("login_email")
login_password = os.getenv("login_password")


def check_if_logged_in(page_driver: WebDriver):
    elements = page_driver.find_elements(
        By.XPATH, f"//span[contains(text(), 'Prisijungti')]"
    )
    if elements:
        return False
    else:
        return True


def login(page_driver: WebDriver):
    if check_if_logged_in(page_driver):
        print("Already logged in")
        return page_driver
    else:
        page_driver = apply_click_on_elements_with_innerHtml(page_driver, "Sutinku")
        time.sleep(0.5)
        page_driver = apply_click_on_elements_with_innerHtml(page_driver, "Prisijungti")
        time.sleep(0.5)
        page_driver = apply_click_on_element_by_class(page_driver, "js-username-field")
        page_driver = type_text_globally(page_driver, login_email)
        page_driver = apply_click_on_elements_with_innerHtml(page_driver, "Tęsti")
        time.sleep(0.5)
        page_driver = type_text_globally(page_driver, login_password)
        time.sleep(0.5)
        page_driver = apply_click_on_elements_with_innerHtml(
            page_driver, "Prisijungti", "button"
        )

        time.sleep(1)
        return page_driver
