from database.tables.tables import Seller
from models.models import Seller as SellerModel


def create_seller(session, seller: SellerModel) -> SellerModel:
    seller = Seller(**seller.dict())
    session.add(seller)
    session.commit()
    return seller


def delete_seller(session, id: str) -> bool:
    seller = session.query(Seller).filter(Seller.id == id).first()
    session.delete(seller)
    session.commit()
    return seller


def update_seller(session, seller: SellerModel) -> SellerModel:
    existing_seller = session.query(Seller).filter(Seller.id == seller.id).first()
    if existing_seller:
        for key, value in seller.dict().items():
            setattr(existing_seller, key, value)
        session.commit()
        return SellerModel.from_orm(existing_seller)
    return None


def get_seller_by_id(session, seller_id: str) -> SellerModel:
    seller = session.query(Seller).filter(Seller.id == seller_id).first()
    if seller:
        return SellerModel.from_orm(seller)
    return None


def get_seller_by_field_value(
    session, field_name: str, field_value: str
) -> SellerModel:
    seller = (
        session.query(Seller).filter(getattr(Seller, field_name) == field_value).first()
    )
    if seller:
        return SellerModel.from_orm(seller)
    return None


def get_seller_by_name_and_email_hash(
    session, name: str, email_hash: str
) -> SellerModel:
    if name and email_hash:
        seller = (
            session.query(Seller)
            .filter(Seller.name == name)
            .filter(Seller.email_hash == email_hash)
            .first()
        )
    if seller:
        return SellerModel.from_orm(seller)
    return None


def get_seller_by_name_and_image_hash(
    session, name: str, image_hash: str
) -> SellerModel:
    if name and image_hash:
        seller = (
            session.query(Seller)
            .filter(Seller.name == name)
            .filter(Seller.image_hash == image_hash)
            .first()
        )
    if seller:
        return SellerModel.from_orm(seller)
    return None


def optimal_seller_finder(session, seller: SellerModel) -> SellerModel | None:
    if seller.name and seller.email_hash:
        existing_seller = get_seller_by_name_and_email_hash(
            session, seller.name, seller.email_hash
        )
        if not existing_seller:
            return None
        return SellerModel.from_orm(existing_seller)
    elif seller.name and seller.image_hash:
        existing_seller = get_seller_by_name_and_image_hash(
            session, seller.name, seller.image_hash
        )
        if existing_seller:
            return SellerModel.from_orm(existing_seller)
    return None


def update_seller_phone_numbers(
    session, seller: SellerModel, number: str
) -> SellerModel:
    if not seller.phone_numbers:
        seller.phone_numbers = [number]
        seller = update_seller(session, seller)
    elif number not in seller.phone_numbers:
        phone_numbers = seller.phone_numbers
        phone_numbers.append(number)
        seller.phone_numbers = phone_numbers
        seller = update_seller(session, seller)
    return seller
