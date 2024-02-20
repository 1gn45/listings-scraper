from database.tables.tables import Vehicle
from models.models import Vehicle as VehicleModel
from database.tables.tables import Vehicle


def create_vehicle(session, vehicle: VehicleModel) -> VehicleModel:
    vehicle = Vehicle(**vehicle.dict())
    session.add(vehicle)
    session.commit()
    return vehicle


def get_vehicle_by_id(session, vehicle_id: str) -> VehicleModel:
    vehicle = session.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    return vehicle


def get_vehicle_by_field_value(
    session, field_name: str, field_value: str
) -> VehicleModel:
    vehicle = (
        session.query(Vehicle)
        .filter(getattr(Vehicle, field_name) == field_value)
        .first()
    )
    return vehicle


def get_vehicle_by_vin_code(session, vin_code: str | None) -> VehicleModel:
    if not vin_code:
        return None
    vehicle = session.query(Vehicle).filter(Vehicle.vin_code == vin_code).first()
    return vehicle
