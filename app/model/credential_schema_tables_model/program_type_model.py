from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class ProgramTypeModel(db.Model):
    """
    Data model for ProgramType DB table.
    """

    __tablename__ = "program_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return ProgramTypeModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            type=self.type,
            external_id=self.external_id,
        )
