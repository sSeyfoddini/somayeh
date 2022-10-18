from app import db
from sqlalchemy import Column
from uuid import uuid4

def uuid():
    return str(uuid4())

class BadgeModel(db.Model):
    """
    Data model for Badge DB table.
    """

    __tablename__ = "badge"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    credential_type_id = Column(db.String, nullable=True)
    credential_type_label = Column(db.String, nullable=True)
    class_id = Column(db.String, nullable=False)
    external_user_id = Column(db.String, nullable=True)
    badge_type_uuid = Column(db.String, nullable=False)
    badge_name = Column(db.String, nullable=True)
    badge_description = Column(db.String, nullable=True)
    badge_org_id = Column(db.String, nullable=True)
    badge_org_label = Column(db.String, nullable=True)
    badge_org_logo = Column(db.String, nullable=True)
    badge_date = Column(db.String, nullable=True)
    badge_external_link = Column(db.String, nullable=True)
    badge_image = Column(db.String, nullable=True)
    badge_json = Column(db.JSON, nullable=True)
    key = Column(db.String, nullable=False)
    learner_uuid = Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "credential_type_id": self.credential_type_id,
            "credential_type_label": self.credential_type_label,
            "class_id": self.class_id,
            "external_user_id": self.external_user_id,
            "badge_type_uuid": self.badge_type_uuid,
            "badge_name": self.badge_name,
            "badge_description": self.badge_description,
            "badge_org_id": self.badge_org_id,
            "badge_org_label": self.badge_org_label,
            "badge_org_logo": self.badge_org_logo,
            "badge_date": self.badge_date,
            "badge_external_link": self.badge_external_link,
            "badge_image": self.badge_image,
            "badge_json": self.badge_json,
            "key": self.key,
            "learner_uuid": self.learner_uuid
        }

    def _clone(self):
        return BadgeModel(
            uuid=self.uuid,
            credential_type_id=self.credential_type_id,
            credential_type_label=self.credential_type_label,
            class_id=self.class_id,
            external_user_id=self.external_user_id,
            badge_type_uuid=self.badge_type_uuid,
            badge_name=self.badge_name,
            badge_description=self.badge_description,
            badge_org_id=self.badge_org_id,
            badge_org_label=self.badge_org_label,
            badge_org_logo=self.badge_org_logo,
            badge_date=self.badge_date,
            badge_external_link=self.badge_external_link,
            badge_image=self.badge_image,
            badge_json=self.badge_json,
            key=self.key,
            learner_uuid=self.learner_uuid
        )
