from uuid import uuid4
from app import db


def uuid():
    return str(uuid4())

class ExperienceTypeModel(db.Model):
    """
    Data model for Experience Type DB table.
    """

    __tablename__ = "experience_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    experience_type_id = db.Column(db.BIGINT, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    org_id = db.Column(db.BIGINT, nullable=False)
    org_name = db.Column(db.String, nullable=False)
    org_logo = db.Column(db.String, nullable=True)
    experience_category_id = db.Column(db.String, nullable=False)
    experience_category = db.Column(db.String, nullable=False)
    experience_subcategory_id = db.Column(db.String, nullable=True)
    experience_subcategory = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "experience_type_id": self.experience_type_id,
            "name": self.name,
            "description": self.description,
            "org_id": self.org_id,
            "org_name": self.org_name,
            "org_logo": self.org_logo,
            "experience_category_id": self.experience_category_id,
            "experience_category": self.experience_category,
            "experience_subcategory_id": self.experience_subcategory_id,
            "experience_subcategory": self.experience_subcategory,
            "image": self.image
        }

    def _clone(self):
        return ExperienceTypeModel(
            uuid=self.uuid,
            experience_type_id=self.experience_type_id,
            name=self.name,
            description=self.description,
            org_id=self.org_id,
            org_name=self.org_name,
            org_logo=self.org_logo,
            experience_category_id=self.experience_category_id,
            experience_category=self.experience_category,
            experience_subcategory_id=self.experience_subcategory_id,
            experience_subcategory=self.experience_subcategory,
            image=self.image
        )
