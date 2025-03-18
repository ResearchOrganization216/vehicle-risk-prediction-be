from app import db
from app.types.policy_holder import PolicyEntry
from sqlalchemy.exc import SQLAlchemyError
from app.services.vehicle_risk_prediction.log_service import save_log

def get_policy_holder_by_user_id(user_id):
    try:
        # Query the POLICY_HOLDERS table for policy holders associated with the user ID
        policy_holder = PolicyEntry.query.filter_by(user_id=user_id).first()

        if not policy_holder:
            return {"error": "No policy holder found for this user"}, 404

        return {"policy_holder": policy_holder.to_dict()}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        save_log(
            levelname="ERROR",
            message="Failed to get policy holder",
            request_data={"user_id": user_id},
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred while fetching policy holder: {str(e)}"}, 500
    
def get_all_policy_holders():
    try:
        # Query the POLICY_HOLDERS table for all policy holders
        policy_holders = PolicyEntry.query.all()

        if not policy_holders:
            return {"error": "No policy holders found in the database"}, 404

        # Convert query result into a list of dictionaries
        policy_holder_list = [policy_holder.to_dict() for policy_holder in policy_holders]
        return {"policy_holders": policy_holder_list}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        save_log(
            levelname="ERROR",
            message="Failed to get all policy holders",
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred while fetching policy holders: {str(e)}"}, 500

