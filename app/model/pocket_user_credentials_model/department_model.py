from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class DepartmentModel(db.Model):
    """
    Data model for department DB table.
    """

    __tablename__ = "department"

    uuid = db.Column(db.String, default=uuid, primary_key=True)
    credential_type_id = db.Column(db.String, nullable=True, index=True)
    department_id = db.Column(db.String, nullable=False, index=True)
    department_label = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=False), nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=True)
    parent_organization = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "credential_type_id": self.credential_type_id,
            "department_id": self.department_id,
            "department_label": self.department_label,
            "date": str(self.date),
            "type": self.type,
            "external_id": self.external_id,
            "parent_organization": self.parent_organization,
        }

    def _clone(self):
        return DepartmentModel(
            uuid=self.uuid,
            credential_type_id=self.credential_type_id,
            department_id=self.department_id,
            department_label=self.department_label,
            date=self.date,
            type=self.type,
            external_id=self.external_id,
            parent_organization=self.parent_organization,
        )
