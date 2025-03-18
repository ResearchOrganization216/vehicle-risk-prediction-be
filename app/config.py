import os
import joblib
import logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:

    # Paths to models
    MODEL_PATHS = {
        'price_model': os.path.join('app', 'models', 'vehicle_risk_prediction','price_model.pkl'),
        'risk_model': os.path.join('app', 'models', 'vehicle_risk_prediction','risk_model.pkl'),
        'spare_parts_model': os.path.join('app', 'models', 'vehicle_risk_prediction','spare_parts_risk_model_random_search.pkl')
    }

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@34.142.175.163:5432/InnoAInsure'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUCKET_NAME = "innoainsure-bucket"
    KEY_PATH = "C:\\Users\\Sithija\\Documents\\keyfiles\\innoainsure-project-531bfaa81104.json"  # Set to an empty string in production
    PROJECT_ID = "innoainsure-project"
    SECRET_KEY = 'your-very-secret-key'

    # Load models
    @staticmethod
    def load_models():
        models = {}
        for key, path in Config.MODEL_PATHS.items():
            models[key] = joblib.load(path)
        return models

class DevelopmentConfig(Config):
    BASE_URL = os.getenv('DEV_BASE_URL', 'http://localhost:5005/api/vehicles')  # Dev URL

class ProductionConfig(Config):
    BASE_URL = os.getenv('PROD_BASE_URL', 'http://35.186.148.98:5005/api/vehicles')  # Prod URL

# Load models when the app starts
models = Config.load_models()
price_model = models['price_model']
risk_model = models['risk_model']
spare_parts_model = models['spare_parts_model']



# Logging Configuration
LOG_FILE = "app/logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
