from datetime import date
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from database.tables.tables import Base, Seller, Vehicle, Listing
import database.crud.seller as seller_crud
import database.crud.vehicle as vehicle_crud
import database.crud.listing as listing_crud

from selenium.webdriver.chrome.webdriver import WebDriver
from dotenv import load_dotenv
import os
from controllers.scraping.listing.listing_data_fetcher import get_all_data_from_listing

import time

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def add_listing(page_driver, url: str, url_field_name: str, page_name: str):
    existing_listing = listing_crud.get_listing_by_url(session, url)
    if not existing_listing:
        seller, vehicle, listing = get_all_data_from_listing(url, page_driver)

        existing_seller = seller_crud.optimal_seller_finder(session, seller)
        if existing_seller:
            existing_seller = seller_crud.update_seller_phone_numbers(
                session, existing_seller, seller.phone_numbers[0]
            )
            listing.seller_id = existing_seller.id
        elif not existing_seller:
            existing_seller = seller_crud.create_seller(session, seller)

        existing_vehicle = vehicle_crud.get_vehicle_by_vin_code(
            session, vehicle.vin_code
        )
        if existing_vehicle:
            listing.vehicle_id = existing_vehicle.id
        elif not existing_vehicle:
            existing_vehicle = vehicle_crud.create_vehicle(session, vehicle)

        if not existing_listing:
            existing_listing = listing_crud.create_listing(session, listing)

    return False
