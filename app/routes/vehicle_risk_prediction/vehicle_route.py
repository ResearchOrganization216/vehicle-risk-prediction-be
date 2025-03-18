from flask import Blueprint, request, jsonify
from app.services.vehicle_risk_prediction.vehicle_service import get_vehicle_by_user_id, get_all_vehicles

# Create a Blueprint for the vehicle routes
vehicle_data_bp = Blueprint('vehicle_data', __name__)

# Route to get vehicles by user ID
@vehicle_data_bp.route('/user/<int:user_id>', methods=['GET'])
def get_vehicle_by_user(user_id):
    try:
        # Call the service to get vehicles by user ID
        result, status_code = get_vehicle_by_user_id(user_id)
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Route to get all vehicles
@vehicle_data_bp.route('/all', methods=['GET'])
def get_all_vehicle():
    try:
        # Call the service to get all vehicles
        result, status_code = get_all_vehicles()
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
