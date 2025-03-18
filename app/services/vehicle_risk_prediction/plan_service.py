from app import db
from app.types.plan_model import PlanEntry
import logging
from datetime import datetime

def save_plan(data):
    try:
        # Extract riskData from the input
        risk_data = data.get("riskData", {})
        timestamp = str(data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        client_id = risk_data.get("client_id") or 0

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
        print(f"Failed to save plan: {e}")
        return {"error": f"An error occurred: {str(e)}"}