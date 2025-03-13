from flask import Blueprint, request, jsonify
from app.services.vehicle_risk_prediction.price_risk_prediction.prediction_service import predict_price_and_risk

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/risk', methods=['POST'])
def predict():
    try:
        data = request.json
        make = data.get('make')
        model = data.get('model')
        vehicle_type = data.get('vehicle_type')
        year = int(data.get('year'))
        mileage = float(data.get('mileage'))

        predicted_price, predicted_risk = predict_price_and_risk(make, model, vehicle_type, year, mileage)

        return jsonify({
            'predicted_price': f"Rs{float(predicted_price):,.2f}",
            'predicted_risk_score': float(predicted_risk)%100
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400
