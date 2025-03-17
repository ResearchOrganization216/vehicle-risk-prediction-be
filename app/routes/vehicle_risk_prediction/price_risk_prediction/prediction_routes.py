from flask import Blueprint, request, jsonify
import logging
from app.services.vehicle_risk_prediction.price_risk_prediction.prediction_service import predict_price_and_risk
from app.utils.vehicle_risk_prediction.price_risk_prediction.validation import validate_input
from app.config import logger

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/risk', methods=['POST'])
def predict():
    try:
        data = request.json
        logger.info(f"Received request: {data}")

        # Validate input
        is_valid, message = validate_input(data)
        if not is_valid:
            logger.warning(f"Validation failed: {message}")
            return jsonify({"error": message}), 400

        make = data["make"]
        model = data["model"]
        vehicle_type = data["vehicle_type"]
        year = int(data["year"])
        mileage = float(data["mileage"])

        predicted_price, predicted_risk = predict_price_and_risk(make, model, vehicle_type, year, mileage)

        response = {
            "predicted_price": f"Rs{float(predicted_price):,.2f}",
            "predicted_risk_score": float(predicted_risk)
        }

        logger.info(f"Prediction successful: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500