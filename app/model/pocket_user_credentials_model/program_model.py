from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class ProgramModel(db.Model):
    """
    Data model for program DB table.
    """

    __tablename__ = "program"

    uuid = db.Column(db.String, default=uuid, primary_key=True)
    credential_type_id = db.Column(db.String, nullable=True, index=True)
    program_id = db.Column(db.String, nullable=False, index=True)
    program_label = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=True)
    program_type_label = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime(timezone=False), nullable=True)
    type = db.Column(db.String, nullable=True)
    parent_organization = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "credential_type_id": self.credential_type_id,
            "program_id": self.program_id,
            "program_label": self.program_label,
            "external_id": self.external_id,
            "program_type_label": self.program_type_label,
            "date": str(self.date),
            "type": self.type,
            "parent_organization": self.parent_organization,
        }

    def _clone(self):
        return ProgramModel(
            credential_type_id=self.credential_type_id,
            program_id=self.program_id,
            program_label=self.program_label,
            external_id=self.external_id,
            program_type_label=self.program_type_label,
            date=self.date,
            type=self.type,
            parent_organization=self.parent_organization,
            uuid=self.uuid,
        )
