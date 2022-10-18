from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class ClassLevelModel(db.Model):
    """
    Data model for ClassLevel DB table.
    """

    __tablename__ = "class_level"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    level = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    semester_order = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "level": self.level,
            "description": self.description,
            "semester_order": self.semester_order,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return ClassLevelModel(
            uuid=self.uuid,
            level=self.level,
            description=self.description,
            semester_order=self.semester_order,
            type=self.type,
            external_id=self.external_id,
        )
