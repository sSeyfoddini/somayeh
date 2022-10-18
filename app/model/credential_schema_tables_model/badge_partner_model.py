from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())


class BadgePartnerModel(db.Model):
    """
    Data model for BadgePartner DB table.
    """

    __tablename__ = "badge_partner"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True, unique=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "url": self.url,
        }

    def _clone(self):
        return BadgePartnerModel(
            uuid=self.uuid,
            name=self.name,
            url=self.url
        )
