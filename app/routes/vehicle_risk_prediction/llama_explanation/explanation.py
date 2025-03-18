import logging
from flask import Blueprint, request, jsonify
from app.config import logger
from app.services.vehicle_risk_prediction.llama_explanation.llama_explanation_service import generate_lama_explanation
from app.services.vehicle_risk_prediction.log_service import save_log

# Initialize the blueprint
lama_explanation_bp = Blueprint('lama_explanation', __name__)

@lama_explanation_bp.route('/insurance/explanation', methods=['POST'])
def get_lama_explanation():
    try:
        # Get the input data from the request
        risk_data = request.json
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        logger.info(f"Received risk data for explanation: {risk_data}")

        # Return the explanation and total risk score in the response
        explanation, total_risk_score, adjusted_premium, adjustment_factor, previous_premium, previous_risk = generate_lama_explanation(risk_data)

        # Return the explanation, total risk score, and adjusted premium in the response
        response = {
            "explanation": explanation,
            "total_risk_score": total_risk_score,
            "adjusted_premium": adjusted_premium,
            "adjustment_factor": adjustment_factor,
            "previous_premium": previous_premium,
            "previous_risk": previous_risk
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error generating LLaMA explanation: {str(e)}", exc_info=True)
        save_log(
            levelname="ERROR",
            message="Error generating LLaMA explanation",
            ip=ip_address,
            request_data=risk_data,
            response_data={"error": str(e)},
            logged_by=user_agent
        )
        return jsonify({"error": "Failed to generate insurance explanation"}), 500
