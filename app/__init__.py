from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Loading configuration
    app.config.from_object('app.config.Config')

    # Initializing extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registering blueprints
    #routes for vehicle risk prediction
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

    # Default route for '/'
    @app.route('/')
    def index():
        return "Welcome to Flask with PostgreSQL!"

    return app
