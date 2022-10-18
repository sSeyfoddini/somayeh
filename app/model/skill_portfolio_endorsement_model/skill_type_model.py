from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class SkillTypeModel(db.Model):
    """
    Data model for SkillType DB table.
    """

    __tablename__ = "skill_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    category_id = db.Column(db.String, nullable=True)
    category_name = db.Column(db.String, nullable=True)
    Updates_for_POCKMMVP_1030 = db.Column(db.String, nullable=True)
    reference_url = db.Column(db.String, nullable=True)
    source_skill_type_id = db.Column(db.String, nullable=True)
    occupation_ids = db.Column(db.String, nullable=True, index=True)
    employer_ids = db.Column(db.String, nullable=True, index=True)
    keywords = db.Column(db.String, nullable=True)
    rsd = db.Column(db.String, nullable=True)
    rsd_uri = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "category_id": eval(self.category_id),
            "category_name": eval(self.category_name),
            "Updates_for_POCKMMVP_1030": self.Updates_for_POCKMMVP_1030,
            "reference_url": self.reference_url,
            "source_skill_type_id": self.source_skill_type_id,
            "occupation_ids": self.occupation_ids,
            "employer_ids": self.employer_ids,
            "keywords": eval(self.keywords),
            "rsd": self.rsd,
            "rsd_uri": self.rsd_uri,
        }

    def _clone(self):
        return SkillTypeModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            category_id=self.category_id,
            category_name=self.category_name,
            reference_url=self.reference_url,
            source_skill_type_id=self.source_skill_type_id,
            occupation_ids=self.occupation_ids,
            employer_ids=self.employer_ids,
            keywords=self.keywords,
            rsd=self.rsd,
            rsd_uri=self.rsd_uri,
        )
