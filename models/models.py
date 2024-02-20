from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class Seller(BaseModel):
    id: UUID | None
    name: str | None
    email: str | None
    email_hash: str | None
    image_hash: str | None
    country: str | None
    city: str | None
    seller_type: str | None
    phone_numbers: List[str] | None
    # listings: List["Listing"] = []

    class Config:
        orm_mode = True
        from_attributes = True


class Vehicle(BaseModel):
    id: UUID | None
    manufacturer: str | None
    model: str | None
    manufacture_year: int | None
    fuel_type: str | None
    engine_cc: int | None
    power_kw: int | None
    body_type: str | None
    driven_wheels: str | None
    gearbox: str | None
    steering_wheel: str | None
    vin_code: str | None
    listings: List["Listing"] = []
    first_registration_date: date | None
    first_registration_country: str | None
    vehicle_type: str | None

    class Config:
        orm_mode = True
        from_attributes = True


class Listing(BaseModel):
    id: UUID | None
    country: str | None
    city: str | None
    sdk_code: str | None
    plate_code: str | None
    vehicle_rida_km: int | None
    listing_start_date: date | None
    listing_end_date: date | None
    description: str | None
    price: float | None
    vehicle_id: UUID | None
    vehicle: Vehicle | None
    seller_id: UUID | None
    seller: Seller | None
    url: str | None
    vehicle_type: str | None
    phone_number: str | None

    class Config:
        orm_mode = True
        from_attributes = True
