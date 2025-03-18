from app import db
from datetime import datetime

class VehicleEntry(db.Model):
    __tablename__ = "VEHICLE_DATA"
    __table_args__ = {"schema": "base"} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(50))
    vehicle_type = db.Column(db.String(50), nullable=False)