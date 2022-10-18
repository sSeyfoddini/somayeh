from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class BadgeObjectModel(db.Model):
    """
    Data model for Badge Object DB table.
    """

    __tablename__ = "badge_object"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    badge_def_uuid = db.Column(db.String, nullable=False)
    learner_uuid = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "badge_def_uuid": self.badge_def_uuid,
            "learner_uuid":self.learner_uuid,
            "status": self.status
        }

    def _clone(self):
        return BadgeObjectModel(
            uuid=self.uuid,
            badge_def_uuid=self.badge_def_uuid,
            learner_uuid=self.learner_uuid,
            status=self.status
        )