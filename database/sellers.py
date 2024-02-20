from database.tables.tables import Base, Seller, Car, Listing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import uuid


def check_if_seller_exists(session, seller_data: dict):
    seller = (
        session.query(Seller)
        .filter(
            Seller.name == seller_data["name"],
            Seller.email == seller_data["email"],
            Seller.phone_number == seller_data["phone_number"],
        )
        .first()
    )
    return seller
