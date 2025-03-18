from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
import os
from app.config import db 

from app.config import DevelopmentConfig, ProductionConfig
migrate = Migrate()

def create_app(config_name=os.getenv('ENVIRONMENT', 'development'), testing=False): 
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.config.Config')

    if config_name == "development":
        app.config.from_object(DevelopmentConfig)
    elif config_name == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Enable testing mode if specified
    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False  

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from app.routes.vehicle_risk_prediction.price_risk_prediction.prediction_routes import prediction_bp
    app.register_blueprint(prediction_bp, url_prefix='/api/vehicles/price')

    from app.routes.vehicle_risk_prediction.spare_risk_prediction.prediction_routes import spare_parts_risk_bp
    app.register_blueprint(spare_parts_risk_bp, url_prefix='/api/vehicles/spare-parts')

    from app.routes.vehicle_risk_prediction.prediction_routes import combined_risk_bp
    app.register_blueprint(combined_risk_bp, url_prefix='/api/vehicles')

    from app.routes.vehicle_risk_prediction.claims_risk.prediction_routes import insurance_claims_bp
    app.register_blueprint(insurance_claims_bp, url_prefix='/api/vehicles')

    from app.routes.vehicle_risk_prediction.llama_explanation.explanation import lama_explanation_bp
    app.register_blueprint(lama_explanation_bp, url_prefix='/api/vehicles')

    from app.routes.vehicle_risk_prediction.plan_data.handleplan_route import plan_data_bp
    app.register_blueprint(plan_data_bp, url_prefix='/api/vehicles')

    # Default route for '/'
    @app.route('/')
    def index():
        return "Welcome to Flask with PostgreSQL!"

    return app
