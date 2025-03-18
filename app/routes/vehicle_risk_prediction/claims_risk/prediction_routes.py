from flask import Blueprint, request, jsonify
from app.utils.vehicle_risk_prediction.claims_risk.validation import validate_insurance_risk_input
from app.services.vehicle_risk_prediction.claims_risk.prediction_service import calculate_insurance_risk
from app.config import logger
from app.services.vehicle_risk_prediction.log_service import save_log

insurance_claims_bp = Blueprint('insurance_claims', __name__)

@insurance_claims_bp.route('/insurance/risk', methods=['POST'])
def insurance_risk():
    try:
        # Parse request data
        data = request.json
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        logger.info(f"Received request for insurance risk: {data}")

        # Validate input
        is_valid, message = validate_insurance_risk_input(data)
        if not is_valid:
            return jsonify({"error": message}), 400

        # Process the request using service
        result = calculate_insurance_risk(data["make"], data["model"])
        if result is None:
            return jsonify({"error": "Failed to calculate insurance risk"}), 500

        logger.info(f"Insurance risk calculated: {result}")
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error during insurance risk calculation: {str(e)}", exc_info=True)
        save_log(
            levelname="ERROR",
            message="Error during insurance risk calculation",
            ip=ip_address,
            request_data=data,
            response_data={"error": str(e)},
            logged_by=user_agent
        )
        return jsonify({"error": "Internal server error"}), 500
