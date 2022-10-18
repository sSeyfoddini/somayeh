from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class MimeTypeModel(db.Model):
    """
    Data model for MimeType DB table.
    """

    __tablename__ = "mime_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    mime_type1 = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "mime_type1": self.mime_type1,
            "extension": self.extension,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return MimeTypeModel(
            uuid=self.uuid,
            mime_type1=self.mime_type1,
            extension=self.extension,
            type=self.type,
            external_id=self.external_id,
        )
