import json
import os
import logging
from threading import Lock
from datetime import datetime

# Define the path to save the JSON data
JSON_FILE_PATH = os.path.join("app", "logs", "vehicle_plans.json")

# Set up logger
logger = logging.getLogger(__name__)

# Initialize a lock for file operations to avoid race conditions
file_lock = Lock()

def save_vehicle_plan(data):
    try:
        # Log the incoming data
        logger.info(f"Received data for saving vehicle plan: {data}")

        # Extract riskData from the input
        risk_data = data.get("riskData", {})
        timestamp = str(data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Prepare the data to be saved, including risk data
        plan_data = {
            "make": data.get("make"),
            "model": data.get("model"),
            "vehicle_type": data.get("vehicle_type"),
            "year": data.get("year"),
            "mileage": data.get("mileage"),
            "timestamp": timestamp,  
            "risk_data": {
                "explanation": risk_data.get("explanation"),
                "predicted_claim_risk_rank": risk_data.get("predicted_claim_risk_rank"),
                "predicted_market_risk_score": risk_data.get("predicted_market_risk_score"),
                "predicted_price": risk_data.get("predicted_price"),
                "predicted_spare_parts_risk_percentage": risk_data.get("predicted_spare_parts_risk_percentage"),
                "premium_adjustment_percentage": risk_data.get("premium_adjustment_percentage"),
                "previous_risk": risk_data.get("previous_risk"),
                "total_risk_score": risk_data.get("total_risk_score"),
            }
        }

        # Ensure the logs directory exists
        log_dir = os.path.dirname(JSON_FILE_PATH)
        if not os.path.exists(log_dir):
            logger.info(f"Directory {log_dir} does not exist. Creating it.")
            os.makedirs(log_dir)

        # Use a lock to ensure thread safety during file operations
        with file_lock:
            # Check if the JSON file exists, if not create it
            if os.path.exists(JSON_FILE_PATH):
                with open(JSON_FILE_PATH, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            # Append the new plan data to the existing data
            existing_data.append(plan_data)

            # Save the updated data to the JSON file
            with open(JSON_FILE_PATH, 'w') as f:
                json.dump(existing_data, f, indent=4)

        logger.info("Vehicle plan saved successfully.")
        return {"message": "Plan accepted and saved successfully"}

    except Exception as e:
        # Log the error
        logger.error(f"An error occurred while saving the vehicle plan: {str(e)}")
        return {"error": f"An error occurred: {str(e)}"}
