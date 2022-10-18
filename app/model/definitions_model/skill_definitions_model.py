from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class SkillDefinitionsModel(db.Model):
    """
    Data model for Skill DB table.
    """

    __tablename__ = "skill_definitions"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    external_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=True)
    reference_url = db.Column(db.String, nullable=True)
    keywords = db.Column(db.String, nullable=True)
    course_code = db.Column(db.String, nullable=True)
    occupation_ids = db.Column(db.String, nullable=True)
    employer_ids = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "external_id": self.external_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "reference_url": self.reference_url,
            "keywords": self.keywords,
            "course_code": self.course_code,
            "occupation_ids": self.occupation_ids,
            "employer_ids": self.employer_ids,
        }

    def _clone(self):
        return SkillDefinitionsModel(
            uuid=self.uuid,
            external_id=self.external_id,
            name=self.name,
            description=self.description,
            category=self.category,
            reference_url=self.reference_url,
            keywords=self.keywords,
            course_code=self.course_code,
            occupation_ids=self.occupation_ids,
            employer_ids=self.employer_ids,
        )
