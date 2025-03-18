from app import db
from app.types.plan_model import PlanEntry
from datetime import datetime
from app.services.vehicle_risk_prediction.log_service import save_log

def save_plan(data):
    try:
        # Extract riskData from the input
        risk_data = data.get("riskData", {})
        timestamp = str(data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        client_id = data.get("id") or 0

        plan_entry = PlanEntry(
            user_id=client_id,
            previous_risk=risk_data.get("previous_risk"),
            previous_premium=risk_data.get("previous_premium"),
            new_risk=risk_data.get("total_risk_score"),
            new_premium=risk_data.get("premium_adjustment"),
            premium_adjustment_percentage=risk_data.get("premium_adjustment_percentage"),
            explanation=risk_data.get("explanation"),
            user_acceptance="pending",
            created_by="admin",
            created_date=datetime.utcnow()
        )
        db.session.add(plan_entry)
        db.session.commit()
        return {"message": "Plan saved successfully"}
    except Exception as e:
        save_log(
            levelname="ERROR",
            message="Failed to save plan",
            request_data=data,
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred: {str(e)}"}


def get_plan_by_user_id(user_id):
    try:
        # Query the PLANS table for plans associated with the user ID
        plans = PlanEntry.query.filter_by(user_id=user_id).all()

        if not plans:
            return {"error": "No plans found for this user"}, 404
        
        return {"plans": [plan.to_dict() for plan in plans]}
    except Exception as e:
        save_log(
            levelname="ERROR",
            message="Failed to get plans",
            request_data={"user_id": user_id},
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred: {str(e)}"}
    
def get_all_plans():
    try:
        # Query the PLANS table for all plans
        plans = PlanEntry.query.all()

        if not plans:
            return {"error": "No plans found in the database"}, 404

        return {"plans": [plan.to_dict() for plan in plans]}
    except Exception as e:
        save_log(
            levelname="ERROR",
            message="Failed to get all plans",
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred: {str(e)}"}
    
#get latest accepted plan for each user
def get_latest_accepted_plans():
    try:
        # Query the PLANS table for the latest accepted plan for each user
        plans = db.session.query(PlanEntry.user_id, PlanEntry.new_risk, PlanEntry.new_premium).filter_by(user_acceptance="accepted").group_by(PlanEntry.user_id).all()

        if not plans:
            return {"error": "No plans found in the database"}, 404

        return {"plans": [{"user_id": plan[0], "new_risk": plan[1], "new_premium": plan[2]} for plan in plans]}
    except Exception as e:
        save_log(
            levelname="ERROR",
            message="Failed to get latest accepted plans",
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred: {str(e)}"}
    
#get latest accepted plan for a specific user
def get_latest_accepted_plan_by_id(user_id):
    try:
        # Query the PLANS table for the latest accepted plan for the given user ID
        plan = PlanEntry.query.filter_by(user_id=user_id, user_acceptance="accepted").order_by(PlanEntry.created_date.desc()).first()

        if not plan:
            return {"error": "No accepted plan found for this user"}, 404

        return {"plan": plan.to_dict()}
    except Exception as e:
        save_log(
            levelname="ERROR",
            message="Failed to get latest accepted plan",
            request_data={"user_id": user_id},
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred: {str(e)}"}

    
def update_plan_acceptance(plan_id, acceptance_status):
    try:
        # Query the PLANS table for the plan with the given ID
        plan = PlanEntry.query.get(plan_id)

        if not plan:
            return {"error": "Plan not found"}, 404
        
        plan.user_acceptance = acceptance_status
        db.session.commit()
        return {"message": "Plan acceptance status updated successfully"}
    except Exception as e:
        save_log(
            levelname="ERROR",
            message="Failed to update plan acceptance status",
            request_data={"plan_id": plan_id, "acceptance_status": acceptance_status},
            response_data={"error": str(e)},
            logged_by="admin"
        )
        return {"error": f"An error occurred: {str(e)}"}
    