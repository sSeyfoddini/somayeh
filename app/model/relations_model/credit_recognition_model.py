from app import db


class CreditRecognitionModel(db.Model):
    """
    Data model for Relation Credit Recognition DB table.
    """

    __tablename__ = "relation_credit_recognition"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    credit_recognition_type_id = db.Column(db.BIGINT, nullable=False)
    credit_recognition_name = db.Column(db.String, nullable=False)
    credit_recognition_category_id = db.Column(db.BIGINT, nullable=False)
    credit_recognition_keywords = db.Column(db.String, nullable=True)
    conferring_credential = db.Column(db.BIGINT, nullable=False)
    conferring_identifier = db.Column(db.BIGINT, nullable=False)
    supporting_credential = db.Column(db.BIGINT, nullable=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "credit_recognition_type_id": self.credit_recognition_type_id,
            "credit_recognition_name": self.credit_recognition_name,
            "credit_recognition_category_id": self.credit_recognition_category_id,
            "credit_recognition_keywords": self.credit_recognition_keywords,
            "conferring_credential": self.conferring_credential,
            "conferring_identifier": self.conferring_identifier,
            "supporting_credential": self.supporting_credential,
        }

    def _clone(self):
        return CreditRecognitionModel(
            id=self.id,
            credit_recognition_type_id=self.credit_recognition_type_id,
            credit_recognition_name=self.credit_recognition_name,
            credit_recognition_category_id=self.credit_recognition_category_id,
            credit_recognition_keywords=self.credit_recognition_keywords,
            conferring_credential=self.conferring_credential,
            conferring_identifier=self.conferring_identifier,
            supporting_credential=self.supporting_credential,
        )
