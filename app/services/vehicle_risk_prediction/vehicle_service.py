from app import db
from app.types.vehicle_model import VehicleEntry 
from sqlalchemy.exc import SQLAlchemyError
from app.services.vehicle_risk_prediction.plan_service import get_latest_accepted_plan_by_id

def get_vehicle_by_user_id(user_id):
    try:
        # Query the VEHICLE_DATA table for vehicles associated with the user ID
        vehicle = VehicleEntry.query.filter_by(user_id=user_id).all()

        if not vehicle:
            return {"error": "No vehicles found for this user"}, 404

        # Convert query result into a list of dictionaries
        vehicles = [
            {
                "id": v.id,
                "user_id": v.user_id,
                "make": v.make,
                "model": v.model,
                "year": v.year,
                "mileage": v.mileage,
                "created_date": v.created_date,
                "created_by": v.created_by,
                "vehicle_type": v.vehicle_type
            } for v in vehicle
        ]
        return {"vehicles": vehicles}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"An error occurred while fetching vehicles: {str(e)}"}, 500
    
def get_all_vehicles():
    try:
        # Query the VEHICLE_DATA table for all vehicles
        vehicles = VehicleEntry.query.all()

        if not vehicles:
            return {"error": "No vehicles found in the database"}, 404

        # Convert query result into a list of dictionaries
        vehicle_list = [
            {
                "id": v.id,
                "user_id": v.user_id,
                "make": v.make,
                "model": v.model,
                "year": v.year,
                "mileage": v.mileage,
                "created_date": v.created_date,
                "created_by": v.created_by,
                "vehicle_type": v.vehicle_type
            } for v in vehicles
        ]
        #get each user's plan latest accepted plan
        for vehicle in vehicle_list:
            plan = get_latest_accepted_plan_by_id(vehicle["user_id"])
            vehicle["plan"] = plan
        return {"vehicles": vehicle_list}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"An error occurred while fetching vehicles: {str(e)}"}, 500
