from app import db


class SkillModel(db.Model):
    """
    Data model for Relation Skill DB table.
    """

    __tablename__ = "relation_skill"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    skill_type_id = db.Column(db.BIGINT, nullable=False)
    skill_name = db.Column(db.String, nullable=False)
    skill_category_id = db.Column(db.BIGINT, nullable=False)
    skill_keywords = db.Column(db.String, nullable=True)
    conferring_credential = db.Column(db.BIGINT, nullable=False)
    conferring_identifier = db.Column(db.BIGINT, nullable=False)
    supporting_credential = db.Column(db.BIGINT, nullable=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "skill_type_id": self.skill_type_id,
            "skill_name": self.skill_name,
            "skill_category_id": self.skill_category_id,
            "skill_keywords": self.skill_keywords,
            "conferring_credential": self.conferring_credential,
            "conferring_identifier": self.conferring_identifier,
            "supporting_credential": self.supporting_credential,
        }

    def _clone(self):
        return SkillModel(
            id=self.id,
            skill_type_id=self.skill_type_id,
            skill_name=self.skill_name,
            skill_category_id=self.skill_category_id,
            skill_keywords=self.skill_keywords,
            conferring_credential=self.conferring_credential,
            conferring_identifier=self.conferring_identifier,
            supporting_credential=self.supporting_credential,
        )
