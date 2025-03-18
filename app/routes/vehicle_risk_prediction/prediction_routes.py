import requests
from flask import Blueprint, request, jsonify, current_app
from app.utils.vehicle_risk_prediction.price_risk_prediction.validation import validate_input
from app.config import logger
from app.services.vehicle_risk_prediction.log_service import save_log


combined_risk_bp = Blueprint('combined_risk', __name__)

@combined_risk_bp.route('/risk', methods=['POST'])
def combined_risk():
    try:
        # Get the input data from the request
        data = request.json
        logger.info(f"Received request: {data}")

        # Validate the input data
        is_valid, message = validate_input(data)
        if not is_valid:
            logger.warning(f"Validation failed: {message}")
            return jsonify({"error": message}), 400

        # Prepare API endpoints
        base_url = "http://35.186.148.98:5005/api/vehicles"


        # Vehicle Market Price Prediction
        price_risk_data = {
            "make": data["make"],
            "model": data["model"],
            "vehicle_type": data["vehicle_type"],
            "year": data["year"],
            "mileage": data["mileage"]
        }
        price_risk_response = requests.post(f"{base_url}/price/risk", json=price_risk_data)
        if price_risk_response.status_code != 200:
            logger.error(f"Price risk prediction failed: {price_risk_response.text}")
            return jsonify({"error": "Price risk prediction failed"}), 500
        price_risk_result = price_risk_response.json()

        # Spare Parts Risk Prediction
        spare_parts_risk_data = {
            "make": data["make"],
            "model": data["model"],
            "vehicle_type": data["vehicle_type"],
            "year": data["year"]
        }
        spare_parts_risk_response = requests.post(f"{base_url}/spare-parts/risk", json=spare_parts_risk_data)
        if spare_parts_risk_response.status_code != 200:
            logger.error(f"Spare parts risk prediction failed: {spare_parts_risk_response.text}")
            return jsonify({"error": "Spare parts risk prediction failed"}), 500
        spare_parts_risk_result = spare_parts_risk_response.json()

        # Insurance Claims Risk Prediction
        insurance_claims_risk_data = {
            "make": data["make"],
            "model": data["model"]
        }
        insurance_claims_risk_response = requests.post(f"{base_url}/insurance/risk", json=insurance_claims_risk_data)
        if insurance_claims_risk_response.status_code != 200:
            logger.error(f"Insurance claims risk prediction failed: {insurance_claims_risk_response.text}")
            return jsonify({"error": "Insurance claims risk prediction failed"}), 500
        insurance_claims_risk_result = insurance_claims_risk_response.json()

        # Extract values from the responses
        predicted_price = price_risk_result.get('predicted_price', 'N/A')
        predicted_market_risk_score = price_risk_result.get('predicted_risk_score', 'N/A')
        predicted_spare_parts_risk_percentage = spare_parts_risk_result.get('predicted_spare_parts_risk_percentage', 'N/A')
        predicted_claim_risk_rank = insurance_claims_risk_result.get('risk_rank', 'N/A')

        # Ensure risk percentage is numeric
        if isinstance(predicted_spare_parts_risk_percentage, str):
            try:
                predicted_spare_parts_risk_percentage = float(predicted_spare_parts_risk_percentage)
            except ValueError:
                predicted_spare_parts_risk_percentage = 'N/A'

        # Build final combined result
        combined_result = {
            "predicted_claim_risk_rank": predicted_claim_risk_rank,
            "predicted_market_risk_score": predicted_market_risk_score,
            "predicted_price": predicted_price,
            "predicted_spare_parts_risk_percentage": predicted_spare_parts_risk_percentage
        }

        logger.info(f"Combined prediction successful: {combined_result}")

        # Send combined result to Lama LLM explanation API
        try:
            explanation_response = requests.post(f"{base_url}/insurance/explanation", json=combined_result)
            if explanation_response.status_code == 200:
                explanation_result = explanation_response.json()
                combined_result["explanation"] = explanation_result.get("explanation", "No explanation available")
                combined_result["total_risk_score"] = explanation_result.get("total_risk_score", "N/A")
                combined_result["premium_adjustment"] = explanation_result.get("adjusted_premium", "N/A")
                combined_result["premium_adjustment_percentage"] = explanation_result.get("adjustment_factor", "N/A")
                combined_result["previous_premium"] = explanation_result.get("previous_premium", "N/A")
                combined_result["previous_risk"] = explanation_result.get("previous_risk", "N/A")
            else:
                logger.error(f"Lama LLM explanation failed: {explanation_response.text}")
                combined_result["explanation"] = "Explanation could not be generated."
        except Exception as e:
            logger.error(f"Error calling Lama LLM API: {str(e)}")
            combined_result["explanation"] = "Explanation service is currently unavailable."

        return jsonify(combined_result)

    except Exception as e:
        logger.error(f"Error during combined prediction: {str(e)}", exc_info=True)
        save_log(
            levelname="ERROR",
            message="Error during combined predictions",
            request_data=data,
            response_data={"error": str(e)}
        )
        return jsonify({"error": "Internal server error"}), 500
