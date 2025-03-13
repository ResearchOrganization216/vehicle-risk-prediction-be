from flask import Blueprint, request, jsonify
from app.services.customer_risk_assesment_google.risk_assesment import process_risk_assessment

risk_assessment_bp = Blueprint('risk_assessment_bp', __name__)

@risk_assessment_bp.route('/risk-assessment-google', methods=['POST'])
def risk_assessment():
    data = request.json

    # Validate input
    required_fields = ["age", "gender", "vehicleType", "totalClaims", 
                       "reason", "premium", "claimAmount", 
                       "insuredPeriod", "riskPercentage"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400

    # Process the risk assessment
    assessment_result = process_risk_assessment(data)

    if assessment_result.get('error'):
        return jsonify({"error": assessment_result['error']}), 500

    return jsonify(assessment_result), 200