from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class CredentialDefinitionModel(db.Model):
    """
    Data model for Credential Definition DB table.
    """

    __tablename__ = "credential_definition"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    cred_def_type = db.Column(db.String, nullable=False)
    cred_def = db.Column(db.String, nullable=False)
    schema = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "cred_def_type": self.cred_def_type,
            "cred_def":self.cred_def,
            "schema": self.schema,
            "name": self.name
        }

    def _clone(self):
        return CredentialDefinitionModel(
            uuid=self.uuid,
            cred_def_type=self.cred_def_type,
            cred_def=self.cred_def,
            schema=self.schema,
            name=self.name,
        )
