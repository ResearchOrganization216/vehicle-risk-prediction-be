import os
import joblib

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/mydatabase')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Paths to models
    MODEL_PATHS = {
        'price_model': os.path.join('app', 'models', 'vehicle_risk_prediction','price_model.pkl'),
        'risk_model': os.path.join('app', 'models', 'vehicle_risk_prediction','risk_model.pkl'),
    }

    # Load models
    @staticmethod
    def load_models():
        models = {}
        for key, path in Config.MODEL_PATHS.items():
            models[key] = joblib.load(path)
        return models

# Load models when the app starts
models = Config.load_models()
price_model = models['price_model']
risk_model = models['risk_model']
