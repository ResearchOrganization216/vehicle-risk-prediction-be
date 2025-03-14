import logging
from flask import Blueprint, request, jsonify
from app.config import logger
from app.services.vehicle_risk_prediction.llama_explanation.llama_explanation_service import generate_lama_explanation

# Initialize the blueprint
lama_explanation_bp = Blueprint('lama_explanation', __name__)

@lama_explanation_bp.route('/insurance/explanation', methods=['POST'])
def get_lama_explanation():
    try:
        # Get the input data from the request
        risk_data = request.json
        logger.info(f"Received risk data for explanation: {risk_data}")

        # Call the service to generate the LLaMA explanation
        explanation = generate_lama_explanation(risk_data)

        # Return the explanation in the response
        return jsonify({"explanation": explanation})

    except Exception as e:
        logger.error(f"Error generating LLaMA explanation: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to generate insurance explanation"}), 500
