from flask import jsonify
import logging

# Set up logger for validation
logger = logging.getLogger(__name__)

def validate_vehicle_data(data):
    # Define required fields for the main vehicle data
    required_fields = ["make", "model", "vehicle_type", "year", "mileage", "riskData"]

    # Check if all required fields are in the incoming data
    if not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        logger.warning(f"Missing required fields: {missing_fields}")
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Check if all required fields are present in riskData
    risk_data = data.get("riskData")
    required_risk_data_fields = [
        "explanation", "predicted_claim_risk_rank", "predicted_market_risk_score", 
        "predicted_price", "predicted_spare_parts_risk_percentage", 
        "premium_adjustment", "premium_adjustment_percentage", "previous_premium", 
        "previous_risk", "total_risk_score"
    ]
    
    if not all(field in risk_data for field in required_risk_data_fields):
        missing_risk_data_fields = [field for field in required_risk_data_fields if field not in risk_data]
        logger.warning(f"Missing required fields in riskData: {missing_risk_data_fields}")
        return jsonify({"error": f"Missing required fields in riskData: {', '.join(missing_risk_data_fields)}"}), 400

    return None  # Data is valid
