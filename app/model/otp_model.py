from datetime import datetime

from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class OtpModel(db.Model):
    """
    Data model for Otp DB table.
    """

    __tablename__ = "otp"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    created_at = db.Column(db.DateTime(), default=datetime.now(),nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    otp = db.Column(db.INTEGER, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "created_at": str(self.created_at),
            "email": self.email,
            "otp": self.otp,
        }

    def _clone(self):
        return OtpModel(uuid=self.uuid, created_at=self.created_at, email=self.email, otp=self.otp)
