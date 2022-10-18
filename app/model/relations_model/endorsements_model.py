from app import db


class EndorsementsModel(db.Model):
    """
    Data model for Relation Endorsements DB table.
    """

    __tablename__ = "relation_endorsements"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    endorsement_type_id = db.Column(db.BIGINT, nullable=False)
    endorsement_name = db.Column(db.String, nullable=False)
    endorsement_category_id = db.Column(db.BIGINT, nullable=False)
    endorsement_keywords = db.Column(db.String, nullable=True)
    conferring_credential = db.Column(db.BIGINT, nullable=False)
    conferring_identifier = db.Column(db.BIGINT, nullable=False)
    supporting_credential = db.Column(db.BIGINT, nullable=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "endorsement_type_id": self.endorsement_type_id,
            "endorsement_name": self.endorsement_name,
            "endorsement_category_id": self.endorsement_category_id,
            "endorsement_keywords": self.endorsement_keywords,
            "conferring_credential": self.conferring_credential,
            "conferring_identifier": self.conferring_identifier,
            "supporting_credential": self.supporting_credential,
        }

    def _clone(self):
        return EndorsementsModel(
            id=self.id,
            endorsement_type_id=self.endorsement_type_id,
            endorsement_name=self.endorsement_name,
            endorsement_category_id=self.endorsement_category_id,
            endorsement_keywords=self.endorsement_keywords,
            conferring_credential=self.conferring_credential,
            conferring_identifier=self.conferring_identifier,
            supporting_credential=self.supporting_credential,
        )
