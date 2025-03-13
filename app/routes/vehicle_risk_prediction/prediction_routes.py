from flask import Blueprint, request, jsonify, current_app
from app.utils.vehicle_risk_prediction.price_risk_prediction.validation import validate_input
from app.config import logger

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

        # Simulate calling the vehicle market price prediction route
        price_risk_data = {
            "make": data["make"],
            "model": data["model"],
            "vehicle_type": data["vehicle_type"],
            "year": data["year"],
            "mileage": data["mileage"]
        }
        
        #current_app.test_client() to simulate the internal POST request
        with current_app.test_client() as client:
            price_risk_response = client.post('/api/vehicles/price/risk', json=price_risk_data)
            if price_risk_response.status_code != 200:
                logger.error(f"Price risk prediction failed: {price_risk_response.text}")
                return jsonify({"error": "Price risk prediction failed"}), 500
            price_risk_result = price_risk_response.json
            logger.info(f"Price risk prediction result: {price_risk_result}")

        # Simulate calling the spare parts risk prediction route
        spare_parts_risk_data = {
            "make": data["make"],
            "model": data["model"],
            "vehicle_type": data["vehicle_type"],
            "year": data["year"]
        }
        
        # Use current_app.test_client() to simulate the internal POST request
        with current_app.test_client() as client:
            spare_parts_risk_response = client.post('/api/vehicles/spare-parts/risk', json=spare_parts_risk_data)
            if spare_parts_risk_response.status_code != 200:
                logger.error(f"Spare parts risk prediction failed: {spare_parts_risk_response.text}")
                return jsonify({"error": "Spare parts risk prediction failed"}), 500
            spare_parts_risk_result = spare_parts_risk_response.json
            logger.info(f"Spare parts risk prediction result: {spare_parts_risk_result}")

            # Simulate calling the insurance claims risk prediction route
        insurance_claims_risk_data = {
            "make": data["make"],
            "model": data["model"]
        }

        # Use current_app.test_client() to simulate the internal POST request
        with current_app.test_client() as client:
            insurance_claims_risk_response = client.post('/api/vehicles/insurance/risk', json=insurance_claims_risk_data)
            if insurance_claims_risk_response.status_code != 200:
                logger.error(f"Insurance claims risk prediction failed: {insurance_claims_risk_response.text}")
                return jsonify({"error": "Insurance claims risk prediction failed"}), 500
            insurance_claims_risk_result = insurance_claims_risk_response.json
            logger.info(f"Insurance claims risk prediction result: {insurance_claims_risk_result}")

        # Extract values from the responses
        predicted_price = price_risk_result.get('predicted_price', 'N/A')
        predicted_market_risk_score = price_risk_result.get('predicted_risk_score', 'N/A')

        # Handle spare parts risk score
        predicted_spare_parts_risk_percentage = spare_parts_risk_result.get('predicted_spare_parts_risk_percentage', 'N/A')

        # If predicted_spare_parts_risk_percentage is an integer, leave it as is, no need for conversion
        if isinstance(predicted_spare_parts_risk_percentage, str):
            try:
                predicted_spare_parts_risk_percentage = float(predicted_spare_parts_risk_percentage)
            except ValueError:
                predicted_spare_parts_risk_percentage = 'N/A'

        # Extract the claim risk rank
        predicted_claim_risk_rank = insurance_claims_risk_result.get('risk_rank', 'N/A')

        # Build final response combining all results
        combined_result = {
            "predicted_claim_risk_rank": predicted_claim_risk_rank,
            "predicted_market_risk_score": predicted_market_risk_score,
            "predicted_price": predicted_price,
            "predicted_spare_parts_risk_percentage": predicted_spare_parts_risk_percentage
        }


        logger.info(f"Combined prediction successful: {combined_result}")
        return jsonify(combined_result)

    except Exception as e:
        logger.error(f"Error during combined prediction: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
