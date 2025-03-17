import pandas as pd
import numpy as np
from app.config import spare_parts_model

def preprocess_text_field(value):
    return pd.Series(value).str.lower().str.replace(r'[^\w]', '', regex=True).iloc[0]

def predict_spare_parts_risk(make, model, vehicle_type, year):

    # Preprocess inputs: Convert to lowercase and remove non-alphanumeric characters
    make = preprocess_text_field(make)
    model = preprocess_text_field(model)
    vehicle_type = preprocess_text_field(vehicle_type)

    # Create input DataFrame
    input_data = pd.DataFrame([{
        'Make': make,
        'Model': model,
        'VehicleType': vehicle_type,
        'Year': year
    }])

    # Predict risk score
    predicted_risk = spare_parts_model.predict(input_data)

    # Convert risk to percentage (assuming 10 is the max score)
    predicted_risk_percentage = (predicted_risk * 100) / 10

    return round(float(predicted_risk_percentage), 2) 
