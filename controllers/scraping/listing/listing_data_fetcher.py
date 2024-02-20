from datetime import datetime
import email
from unicodedata import name
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from controllers.scraping.common.apply_actions_on_page import (
    apply_click_on_elements_with_innerHtml,
)
from controllers.fetch_page import fetch_page
from controllers.scraping.initiation.login import login
from models.models import Listing, Vehicle, Seller
import requests
import imagehash
from uuid import uuid4
import base64
from PIL import Image
from io import BytesIO
import re

import time


def get_all_data_from_listing(url, driver: WebDriver = None):
    url = url
    driver = fetch_page(url, driver)
    driver = login(driver)
    driver = apply_click_on_elements_with_innerHtml(driver, "Atsisakyti visų")
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")

    seller = get_seller_data_from_html(soup)
    vehicle, listing = fetch_full_vehicle_data_from_page_url(driver, seller)

    (
        seller.image_hash,
        seller.email_hash,
        seller.name,
    ) = get_seller_picture_and_name_from_driver(driver)

    return seller, vehicle, listing


def get_image_hash(image_url: str):
    response = requests.get(image_url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        image = image.resize((8, 8), resample=Image.Resampling.LANCZOS)

        hash_value = imagehash.phash(image)

        hash_str = str(hash_value)

        return hash_str
    else:
        print(f"Failed to fetch image from {image_url}")
        return None


def get_seller_picture_and_name_from_driver(driver: WebDriver):
    def gravatar_email_hash_extractor(url: str) -> str:
        pattern = r"/avatar/([a-fA-F0-9]+)\.jpg"
        match = re.search(pattern, url)
        if match:
            email_hash = match.group(1)
            return email_hash
        else:
            return None

    driver = apply_click_on_elements_with_innerHtml(driver, "Teirautis")
    time.sleep(1)
    driver = apply_click_on_elements_with_innerHtml(driver, "Teirautis")
    try:
        img_element = driver.find_element(By.CLASS_NAME, "messenger__avatar")
        email_hash = gravatar_email_hash_extractor(img_element.get_attribute("src"))
        name_element = driver.find_element(By.ID, "messenger__two-rows-first-id")
        name = name_element.get_attribute("innerHTML")

        image_hash = None
        if not email_hash:
            image_hash = get_image_hash(img_element.get_attribute("src"))

        # with open(f"images/{email_hash}.jpg", "wb") as file:
        #     file.write(image_jpg)
    except Exception as e:
        driver = apply_click_on_elements_with_innerHtml(driver, "Teirautis")
        time.sleep(1)
        img_element = driver.find_element(By.CLASS_NAME, "messenger__avatar")
        email_hash = gravatar_email_hash_extractor(img_element.get_attribute("src"))
        name_element = driver.find_element(By.ID, "messenger__two-rows-first-id")
        name = name_element.get_attribute("innerHTML").strip()

        image_hash = None
        if not email_hash:
            image_hash = get_image_hash(img_element.get_attribute("src"))

    return image_hash, email_hash, name


def get_location_data_from_html(soup: BeautifulSoup):
    seller_location = soup.find("span", class_="seller-contact-location").text.strip()
    if "," in seller_location:
        city, country = seller_location.split(",")
        return city, country
    else:
        return None, seller_location


def get_seller_data_from_html(soup: BeautifulSoup):
    seller = Seller(
        id=uuid4(),
        name=None,
        seller_type=None,
        email=None,
        email_hash=None,
        image_hash=None,
        phone_numbers=None,
        city=None,
        country=None,
    )
    seller.name = soup.find("span", class_="seller-contact-name").text.strip()
    seller.city, seller.country = get_location_data_from_html(soup)
    seller.phone_numbers = [
        soup.find(
            "div", class_="button seller-phone-number js-phone-number"
        ).text.strip()
    ]

    if seller.name in ["Privatus pardavėjas", "Pardavėjas"]:
        seller.seller_type = "private"
        seller.name = None
    else:
        seller.seller_type = "company"
    return seller


def get_manufacturer_from_html(soup: BeautifulSoup):
    crumbs = soup.find_all("li", class_="crumb")
    manufacturer = crumbs[2].text if len(crumbs) > 2 else None
    if manufacturer:
        return manufacturer.strip()
    return None


def get_model_from_html(soup: BeautifulSoup):
    crumbs = soup.find_all("li", class_="crumb")
    model = crumbs[3].text if len(crumbs) > 3 else None
    if model:
        return model.strip()
    return None


def get_vehicle_type_from_html(soup: BeautifulSoup):
    crumbs = soup.find_all("li", class_="crumb")
    model = crumbs[1].text if len(crumbs) > 3 else None
    if model:
        return model.strip()
    return None


def get_multiple_values_from_html(soup: BeautifulSoup, class_name: str):
    parameters = soup.find_all("div", class_=class_name)

    data = {}
    for parameter in parameters:
        key_div = parameter.find("div", class_="parameter-label")
        value_div = parameter.find("div", class_="parameter-value")
        if key_div and value_div:
            key = key_div.text.strip()
            value = value_div.text.strip()
            data[key] = value
    return data


def get_vin_and_sdk_values(driver: WebDriver):
    try:
        show_vin_btn = driver.find_element(By.CLASS_NAME, "vin-parameter")
    except:
        show_vin_btn = None
    if show_vin_btn:
        try:
            time.sleep(3)
            show_vin_btn.click()
            time.sleep(1)
        except:
            print(
                'error happens when "accept cookies" prompt has just loaded and page is disabled'
            )
            driver = apply_click_on_elements_with_innerHtml(driver, "Sutinku")
            return get_vin_and_sdk_values(driver)

    try:
        show_sdk_btn = driver.find_element(By.CLASS_NAME, "sdk-parameter")
    except:
        show_sdk_btn = None
    if show_sdk_btn:
        try:
            time.sleep(3)
            show_sdk_btn.click()
            time.sleep(1)
        except:
            print(
                'error happens when "accept cookies" prompt has just loaded and page is disabled'
            )
            driver = apply_click_on_elements_with_innerHtml(driver, "Sutinku")
            return get_vin_and_sdk_values(driver)

    if show_vin_btn or show_sdk_btn:
        time.sleep(1)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")

    vin = None
    if show_vin_btn:
        vin_div = soup.find("div", class_="vin-parameter")
        vin = vin_div.text if vin_div else None
        if len(vin) != 17 or "." in vin:
            print("VIN is not valid, returning none instead")
            vin = None

    sdk = None
    if show_sdk_btn:
        sdk_div = soup.find("div", class_="sdk-parameter")
        sdk = sdk_div.text if sdk_div else None

    with open("q.html", "w") as file:
        file.write(page_html)

    return vin, sdk


def get_description_from_html(soup: BeautifulSoup):
    description_div = soup.find("div", class_="announcement-description")
    if description_div:
        return description_div.text.strip()
    return None


def get_price_from_html(soup: BeautifulSoup):
    price_div = soup.find("div", class_="price")
    print("price_div: ", price_div)

    if price_div:
        price_text = price_div.get_text(strip=True).replace(" ", "")
        print("price_text: ", price_text)
        numeric_match = re.match(r"\d+", price_text)

        if numeric_match:
            numeric_part = numeric_match.group()
            print("Numeric part:", numeric_part)
            # If you want to convert it to an integer
            numeric_value = int(numeric_part)
            print("Numeric value:", numeric_value)
            return int(numeric_value)
        else:
            print("No leading numeric characters found.")
    return None


def format_date(date_string: str):
    if not date_string:
        return None

    if len(date_string) == 4:
        # If only the year is provided, add month and day as 01
        date_string += "-01-01"
    elif len(date_string) == 7:
        # If only the year and month are provided, add day as 01
        date_string += "-01"

    date_format = "%Y-%m-%d"

    try:
        # Convert the string to a datetime object
        datetime_object = datetime.strptime(date_string, date_format)
        return datetime_object
    except ValueError:
        # Handle the case where the input string is not in the expected format
        print("Invalid date format")
        return None


def get_kw_from_string(string: str | None):
    # string example: "3456 cm³, 310 AG (228kW)"
    if not string:
        return None
    match = re.search(r"\((\d+)kW\)", string)
    if match:
        return int(match.group(1))
    else:
        return None


def fetch_full_vehicle_data_from_page_url(driver: WebDriver, seller: Seller):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    vehicle_type = get_vehicle_type_from_html(soup)
    data_dict = get_multiple_values_from_html(soup, "parameter-row")
    vin, sdk = get_vin_and_sdk_values(driver)

    def get_engine_data_from_data_dict(data_dict: dict):
        if data_dict.get("Variklis"):
            engine_cc = data_dict.get("Variklis").split(" ")[0]
            return engine_cc
        return None

    vehicle = Vehicle(
        id=uuid4(),
        manufacturer=get_manufacturer_from_html(soup),
        model=get_model_from_html(soup),
        manufacture_year=None,
        fuel_type=data_dict.get("Kuro tipas"),
        engine_cc=get_engine_data_from_data_dict(data_dict),
        power_kw=get_kw_from_string(data_dict.get("Variklis")),
        body_type=data_dict.get("Kėbulo tipas"),
        driven_wheels=data_dict.get("Varantieji ratai"),
        gearbox=data_dict.get("Pavarų dėžė"),
        steering_wheel=data_dict.get("Vairo padėtis"),
        vin_code=vin,
        first_registration_date=format_date(data_dict.get("Pirma registracija")),
        first_registration_country=data_dict.get("Pirmosios registracijos šalis"),
        vehicle_type=vehicle_type,
    )

    listing_city, listing_country = get_location_data_from_html(soup)
    listing = Listing(
        id=uuid4(),
        country=listing_country,
        city=listing_city,
        sdk_code=sdk,
        plate_code=None,
        vehicle_rida_km=data_dict.get("Rida").replace("km", "").replace(" ", ""),
        listing_start_date=None,
        listing_end_date=None,
        description=get_description_from_html(soup),
        vehicle_type=vehicle_type,
        price=get_price_from_html(soup),
        vehicle_id=vehicle.id,
        vehicle=vehicle,
        seller_id=seller.id,
        seller=seller,
        url=driver.current_url,
        phone_number=seller.phone_numbers[0],
    )

    return vehicle, listing
