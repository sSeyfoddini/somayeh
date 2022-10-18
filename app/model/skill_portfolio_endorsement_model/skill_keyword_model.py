from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class SkillKeywordModel(db.Model):
    """
    Data model for SkillKeyword DB table.
    """

    __tablename__ = "skill_keyword"

    keyword = db.Column(db.String, nullable=False, primary_key=True)
    uuid = db.Column(db.String, primary_key=True, default=uuid)

    def _to_dict(self):
        return {"uuid": self.uuid, "keyword": self.keyword}

    def _clone(self):
        return SkillKeywordModel(keyword=self.keyword, uuid=self.uuid)
