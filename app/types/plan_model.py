from app import db
from datetime import datetime

class PlanEntry(db.Model):
    __tablename__ = "PLANS"
    __table_args__ = {"schema": "base"}  # Specify schema

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)  # User ID
    previous_risk = db.Column(db.Numeric(10, 2), nullable=False)  # Previous risk score
    previous_premium = db.Column(db.Numeric(12, 2), nullable=False)  # Previous premium amount
    new_risk = db.Column(db.Numeric(10, 2), nullable=False)  # New risk score
    new_premium = db.Column(db.Numeric(12, 2), nullable=False)  # New premium amount
    premium_adjustment_percentage = db.Column(db.String(50))  # Premium adjustment percentage
    user_acceptance = db.Column(db.String(10))  # User acceptance status
    explanation = db.Column(db.Text)  # Explanation for the change
    created_date = db.Column(db.DateTime, default=datetime.utcnow)  # Creation time
    created_by = db.Column(db.String(50)) # User who created the plan

