from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class CollegeModel(db.Model):
    """
    Data model for College DB table.
    """

    __tablename__ = "college"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    credential_type_id = db.Column(db.String, nullable=True)
    college_id = db.Column(db.String, nullable=False, index=True)
    college_label = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=False), nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=True)
    parent_organization = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "credential_type_id": self.credential_type_id,
            "college_id": self.college_id,
            "college_label": self.college_label,
            "date": str(self.date),
            "type": self.type,
            "external_id": self.external_id,
            "parent_organization": self.parent_organization,
        }

    def _clone(self):
        return CollegeModel(
            uuid=self.uuid,
            credential_type_id=self.credential_type_id,
            college_id=self.college_id,
            college_label=self.college_label,
            date=self.date,
            type=self.type,
            external_id=self.external_id,
            parent_organization=self.parent_organization,
        )
