from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class CourseworkTypeModel(db.Model):
    """
    Data model for CourseworkType DB table.
    """

    __tablename__ = "coursework_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return CourseworkTypeModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            type=self.type,
            external_id=self.external_id,
        )
