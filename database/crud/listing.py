from models.models import Listing as ListingModel
from database.tables.tables import Listing


def create_listing(session, listing: ListingModel) -> ListingModel:
    listing = Listing(
        id=listing.id,
        country=listing.country,
        city=listing.city,
        sdk_code=listing.sdk_code,
        plate_code=listing.plate_code,
        vehicle_rida_km=listing.vehicle_rida_km,
        listing_start_date=listing.listing_start_date,
        listing_end_date=listing.listing_end_date,
        description=listing.description,
        price=listing.price,
        vehicle_id=listing.vehicle_id,
        vehicle_type=listing.vehicle_type,
        seller_id=listing.seller_id,
        url=listing.url,
        phone_number=listing.phone_number,
    )
    session.add(listing)
    session.commit()
    return listing


def get_listing_by_id(session, listing_id: str) -> ListingModel:
    listing = session.query(Listing).filter(Listing.id == listing_id).first()
    return listing


def get_listing_by_field_value(
    session, field_name: str, field_value: str
) -> ListingModel:
    listing = (
        session.query(Listing)
        .filter(getattr(Listing, field_name) == field_value)
        .first()
    )
    return listing


def get_listing_by_url(session, url: str) -> ListingModel:
    listing = session.query(Listing).filter(Listing.url == url).first()
    return listing
