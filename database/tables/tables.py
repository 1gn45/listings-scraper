from typing import Any
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    JSON,
    String,
    ForeignKey,
    Text,
    Date,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import date
import os

# Read the DATABASE_URL from the .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()


class Seller(Base):
    __tablename__ = "seller"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    email_hash = Column(String(255), nullable=True)
    image_hash = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    seller_type = Column(String(255), nullable=True)
    phone_numbers = Column(JSON, nullable=True)
    listings = relationship("Listing", back_populates="seller")


class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    manufacturer = Column(String(255))
    model = Column(String(255))
    manufacture_year = Column(Integer)
    fuel_type = Column(String(255))
    engine_cc = Column(Integer)
    power_kw = Column(Integer)
    body_type = Column(String(255))
    driven_wheels = Column(String(255))
    gearbox = Column(String(255))
    steering_wheel = Column(String(255))
    vehicle_type = Column(String(255))

    first_registration_date = Column(Date)
    first_registration_country = Column(String(255))

    vin_code = Column(String(255))

    listings = relationship("Listing", back_populates="vehicle")


class Listing(Base):
    __tablename__ = "listing"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    country = Column(String(255))
    city = Column(String(255))

    sdk_code = Column(String(255))
    plate_code = Column(String(255))
    vehicle_rida_km = Column(Integer)

    listing_start_date = Column(Date)
    listing_end_date = Column(Date)

    description = Column(Text)
    price = Column(Integer)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicle.id"))
    vehicle = relationship("Vehicle", back_populates="listings")
    vehicle_type = Column(String(255))

    seller_id = Column(UUID(as_uuid=True), ForeignKey("seller.id"))
    seller = relationship("Seller", back_populates="listings")

    phone_number = Column(String(255))

    url = Column(String(255), nullable=True)


# Create the tables in the database
Base.metadata.create_all(engine)
