from app import db


class CourseworkModel(db.Model):
    """
    Data model for Relation Coursework DB table.
    """

    __tablename__ = "relation_coursework"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    coursework_type_id = db.Column(db.BIGINT, nullable=False)
    coursework_name = db.Column(db.String, nullable=False)
    coursework_category_id = db.Column(db.BIGINT, nullable=False)
    coursework_keywords = db.Column(db.String, nullable=True)
    conferring_credential = db.Column(db.BIGINT, nullable=False)
    conferring_identifier = db.Column(db.BIGINT, nullable=False)
    supporting_credential = db.Column(db.BIGINT, nullable=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "coursework_type_id": self.coursework_type_id,
            "coursework_name": self.coursework_name,
            "coursework_category_id": self.coursework_category_id,
            "coursework_keywords": self.coursework_keywords,
            "conferring_credential": self.conferring_credential,
            "conferring_identifier": self.conferring_identifier,
            "supporting_credential": self.supporting_credential,
        }

    def _clone(self):
        return CourseworkModel(
            id=self.id,
            coursework_type_id=self.coursework_type_id,
            coursework_name=self.coursework_name,
            coursework_category_id=self.coursework_category_id,
            coursework_keywords=self.coursework_keywords,
            conferring_credential=self.conferring_credential,
            conferring_identifier=self.conferring_identifier,
            supporting_credential=self.supporting_credential,
        )
