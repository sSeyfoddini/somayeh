from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class TitleTypeModel(db.Model):
    """
    Data model for TitleType DB table.
    """

    __tablename__ = "title_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    reference_url = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "reference_url": self.reference_url,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return TitleTypeModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            reference_url=self.reference_url,
            type=self.type,
            external_id=self.external_id,
        )
