from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class ProgramCompletionModel(db.Model):
    """
    Data model for ProgramCompletion DB table.
    """

    __tablename__ = "program_completion"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    credential_type_id = db.Column(db.BIGINT, nullable=False, index=True)
    credential_type_label = db.Column(db.String, nullable=False)
    recognition_date = db.Column(db.DateTime(timezone=False), nullable=False)
    term_id = db.Column(db.BIGINT, nullable=False, index=True)
    term_label = db.Column(db.String, nullable=False)
    program_id = db.Column(db.BIGINT, nullable=False, index=True)
    program_label = db.Column(db.String, nullable=False)
    credential_label = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "credential_type_id": self.credential_type_id,
            "credential_type_label": self.credential_type_label,
            "recognition_date": str(self.recognition_date),
            "term_id": self.term_id,
            "term_label": self.term_label,
            "program_id": self.program_id,
            "program_label": self.program_label,
            "credential_label": self.credential_label,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return ProgramCompletionModel(
            uuid=self.uuid,
            credential_type_id=self.credential_type_id,
            credential_type_label=self.credential_type_label,
            recognition_date=self.recognition_date,
            term_id=self.term_id,
            term_label=self.term_label,
            program_id=self.program_id,
            program_label=self.program_label,
            credential_label=self.credential_label,
            type=self.type,
            external_id=self.external_id,
        )
