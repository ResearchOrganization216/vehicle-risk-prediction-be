from app import db
from datetime import datetime

class LogEntry(db.Model):
    __tablename__ = "LOGS"
    __table_args__ = {"schema": "base"}  # Specify schema

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asctime = db.Column(db.DateTime, default=datetime.utcnow)  # Log timestamp
    levelname = db.Column(db.String(20), nullable=False)  # Log level
    message = db.Column(db.Text, nullable=False)  # Log message
    ip = db.Column(db.String(45))  # IP Address
    request_data = db.Column(db.JSON)  # JSON request payload
    response_data = db.Column(db.JSON)  # JSON response payload
    logged_by = db.Column(db.String(50))  # User who triggered the log
    created_date = db.Column(db.DateTime, default=datetime.utcnow)  # Creation time
