from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class BadgeDefinitionModel(db.Model):
    """
    Data model for Badge Definition DB table.
    """

    __tablename__ = "badge_definition"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    badge_id = db.Column(db.BIGINT, nullable=False)
    badge_name = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {"uuid": self.uuid, "badge_id": self.badge_id, "badge_name": self.badge_name}

    def _clone(self):
        return BadgeDefinitionModel(uuid=self.uuid, badge_id=self.badge_id, badge_name=self.badge_name)
