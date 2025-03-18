from app import db
from app.types.log_model import LogEntry
from datetime import datetime

def save_log(levelname, message, ip=None, request_data=None, response_data=None, logged_by=None):
    try:
        log_entry = LogEntry(
            levelname=levelname,
            message=message,
            ip=ip,
            request_data=request_data,
            response_data=response_data,
            logged_by=logged_by,
            created_date=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        print(f"Failed to save log: {e}")  # Fallback logging
