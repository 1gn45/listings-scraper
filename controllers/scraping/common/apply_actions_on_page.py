from cgitb import html
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time


from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException


def type_text_globally(driver: WebDriver, text: str) -> WebDriver:
    actions = ActionChains(driver)
    actions.send_keys(text).perform()
    return driver


def apply_click_on_element_by_class(driver: WebDriver, class_name: str) -> WebDriver:
    element = driver.find_element(By.CLASS_NAME, class_name)
    element.click()
    return driver


def apply_click_on_element_by_id(driver: WebDriver, id: str) -> WebDriver:
    element = driver.find_element(By.ID, id)
    element.click()
    return driver


def apply_click_on_elements_with_innerHtml(
    driver: WebDriver, innerHtml: str, tag_name: str = None
) -> WebDriver:
    try:
        if tag_name:
            elements = driver.find_elements(
                By.XPATH, f"//{tag_name}[contains(text(), '{innerHtml}')]"
            )
        else:
            elements = driver.find_elements(
                By.XPATH, f"//*[contains(text(), '{innerHtml}')]"
            )
        for element in elements:
            element.click()
        return driver

    # except ElementNotInteractableException:
    #     print("=========== ElementNotInteractableException ===========")
    #     parent_element = element.find_element(By.XPATH, '..')  # Select the parent element
    #     parent_element.click()
    #     return driver

    except Exception as e:
        print("ERROR HAPPENED: ", e)
        if innerHtml == "Sutinku":
            time.sleep(2)
            html = driver.page_source
            with open("q.html", "w") as file:
                file.write(html)
            elements = driver.find_elements(
                By.XPATH, f"//*[contains(text(), '{innerHtml}')]"
            )
            for element in elements:
                element.click()
        else:
            print("=== raising error ===")
            print("ELEMENTS: ", elements)
            raise e
        return driver
