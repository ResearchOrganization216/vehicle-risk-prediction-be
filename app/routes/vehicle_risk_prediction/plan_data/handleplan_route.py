from flask import Blueprint, request, jsonify
from app.services.vehicle_risk_prediction.plan_data.handleplan_service import save_vehicle_plan  # Import the service
from app.utils.vehicle_risk_prediction.plan_data.validation import validate_vehicle_data  # Import validation function
import logging
from app.services.vehicle_risk_prediction.plan_service import save_plan

# Create a Blueprint for the vehicle routes
plan_data_bp = Blueprint('vehicle', __name__)

# Set up logger for this module
logger = logging.getLogger(__name__)

# Endpoint to accept the vehicle plan data
@plan_data_bp.route('/accept-plan', methods=['POST'])
def accept_plan():
    try:
        # Log the incoming request
        logger.info("Received request to accept vehicle plan.")

        # Get the request data
        data = request.get_json()

        if not data:
            logger.warning("No data provided in the request.")
            return jsonify({"error": "No data provided"}), 400

        # Validate the incoming data using the validation function
        validation_error = validate_vehicle_data(data)
        if validation_error:
            return validation_error

        # Call the service to save the vehicle plan
        result = save_vehicle_plan(data)

        # set values and Save the plan to the database
        dbresult = save_plan(data)
        if dbresult is None:
            return jsonify({"error": "Failed to save vehicle plan"}), 500
        logger.info("Vehicle plan processed successfully.")
        # Return the result from the service
        return jsonify(dbresult), 200

    except Exception as e:
        logger.error(f"An error occurred while processing the vehicle plan: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
