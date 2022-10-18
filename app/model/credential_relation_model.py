from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class CredentialRelationModel(db.Model):
    """
    Data model for Credential Relation DB table.
    """

    __tablename__ = "credential_relation"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    relation_type = db.Column(db.String, nullable=False)
    target_cred_type_uuid = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "relation_type": self.relation_type,
            "target_cred_type_uuid":self.target_cred_type_uuid
        }

    def _clone(self):
        return CredentialRelationModel(
            uuid=self.uuid,
            relation_type=self.relation_type,
            target_cred_type_uuid=self.target_cred_type_uuid
        )
