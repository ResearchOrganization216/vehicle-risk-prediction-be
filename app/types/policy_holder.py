from app import db
from datetime import datetime

class PolicyEntry(db.Model):
    __tablename__ = 'POLICY_HOLDERS'
    __table_args__ = {"schema": "base"} 

    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the policy holder
    user_id = db.Column(db.Integer, nullable=False)  # User ID linked to the policy holder
    name = db.Column(db.String(100), nullable=False)  # Name of the policy holder
    address = db.Column(db.Text)  # Address of the policy holder
    policy_renewal_date = db.Column(db.Date)  # Policy renewal date
    contact_number = db.Column(db.String(15))  # Contact number
    nic = db.Column(db.String(20))  # NIC (National Identity Card)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation time
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last updated time
    created_by = db.Column(db.String(50), nullable=False)


    def to_dict(self):
        """
        Convert the PolicyEntry object to a dictionary.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "address": self.address,
            "policy_renewal_date": self.policy_renewal_date.isoformat() if self.policy_renewal_date else None,
            "contact_number": self.contact_number,
            "nic": self.nic,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by
        }
    