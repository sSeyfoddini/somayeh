from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class GradeModel(db.Model):
    """
    Data model for Grade DB table.
    """

    __tablename__ = "grade"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    letter = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "letter": self.letter,
            "value": self.value,
            "description": self.description,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return GradeModel(
            uuid=self.uuid,
            letter=self.letter,
            value=self.value,
            description=self.description,
            type=self.type,
            external_id=self.external_id,
        )
