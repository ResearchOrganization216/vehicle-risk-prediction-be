import pandas as pd
import numpy as np
from app.config import price_model, risk_model 

def preprocess_text_field(value):
    return pd.Series(value).str.lower().str.replace(r'[^\w]', '', regex=True).iloc[0]

def predict_price_and_risk(make, model, vehicle_type, year, mileage):
    # Preprocess text fields
    make = preprocess_text_field(make)
    model = preprocess_text_field(model)
    vehicle_type = preprocess_text_field(vehicle_type)

    # Compute derived features
    vehicle_age = 2024 - year
    mileage_per_year = mileage / vehicle_age if vehicle_age > 0 else mileage

    # Create input DataFrame for price prediction
    input_price_data = pd.DataFrame([{
        'Make': make,
        'Model': model,
        'VehicleType': vehicle_type,
        'VehicleAge': vehicle_age,
        'Mileage': mileage,
        'Mileage_per_year': mileage_per_year
    }])

    # Predict price
    predicted_price_log = price_model.predict(input_price_data)
    predicted_price = np.expm1(predicted_price_log)  # Reverse log1p transformation

    # Prepare data for risk score prediction
    risk_input_data = pd.DataFrame({
        'PredictedPrice': [predicted_price_log[0]],  # Use log-transformed predicted price
        'Year': [year],
        'Mileage': [mileage]
    })

    # Predict risk score
    predicted_risk = risk_model.predict(risk_input_data)[0]

    return predicted_price[0], predicted_risk
