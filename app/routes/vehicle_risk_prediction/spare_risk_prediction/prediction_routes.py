from flask import Blueprint, request, jsonify
import logging
from app.services.vehicle_risk_prediction.spare_risk_prediction.prediction_service import predict_spare_parts_risk
from app.utils.vehicle_risk_prediction.spare_risk_prediction.validation import validate_spare_parts_risk_input
from app.config import logger

spare_parts_risk_bp = Blueprint('spare_parts_risk', __name__)

@spare_parts_risk_bp.route('/risk', methods=['POST'])
def spare_parts_risk():
    try:
        data = request.json
        logger.info(f"Received request: {data}")

        # Validate input
        is_valid, message = validate_spare_parts_risk_input(data)
        if not is_valid:
            logger.warning(f"Validation failed: {message}")
            return jsonify({"error": message}), 400

        # Extract validated data
        make = data["make"]
        model = data["model"]
        vehicle_type = data["vehicle_type"]
        year = int(data["year"])

        # Predict risk
        predicted_risk = predict_spare_parts_risk(make, model, vehicle_type, year)

        response = {
            "predicted_spare_parts_risk_percentage": round(predicted_risk, 2)
        }

        logger.info(f"Prediction successful: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
