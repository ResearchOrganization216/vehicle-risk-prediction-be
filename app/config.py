import os
import joblib
import logging

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/mydatabase')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Paths to models
    MODEL_PATHS = {
        'price_model': os.path.join('app', 'models', 'vehicle_risk_prediction','price_model.pkl'),
        'risk_model': os.path.join('app', 'models', 'vehicle_risk_prediction','risk_model.pkl'),
        'spare_parts_model': os.path.join('app', 'models', 'vehicle_risk_prediction','spare_parts_risk_model_random_search.pkl')
    }

    # Load models
    @staticmethod
    def load_models():
        models = {}
        for key, path in Config.MODEL_PATHS.items():
            models[key] = joblib.load(path)
        return models
    
    BASE_URL = 'http://localhost:5000/api/vehicles'  

class DevelopmentConfig(Config):
    BASE_URL = os.getenv('DEV_BASE_URL', 'http://localhost:5000/api/vehicles')  # Dev URL

class ProductionConfig(Config):
    BASE_URL = os.getenv('PROD_BASE_URL', 'https://prod.api.com/api/vehicles') 

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
