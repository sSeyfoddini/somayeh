from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class TermModel(db.Model):
    """
    Data model for Term DB table.
    """

    __tablename__ = "term"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime(timezone=False), nullable=False)
    end_date = db.Column(db.DateTime(timezone=False), nullable=False)
    session_id = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)
    credential_type_id = db.Column(db.String, nullable=True)
    parent_organization = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "session_id": self.session_id,
            "type": self.type,
            "external_id": self.external_id,
            "credential_type_id": self.credential_type_id,
            "parent_organization": self.parent_organization,
        }

    def _clone(self):
        return TermModel(
            uuid=self.uuid,
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
            session_id=self.session_id,
            type=self.type,
            external_id=self.external_id,
            credential_type_id=self.credential_type_id,
            parent_organization=self.parent_organization,
        )
