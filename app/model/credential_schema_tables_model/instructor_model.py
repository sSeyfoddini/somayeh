from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class InstructorModel(db.Model):
    """
    Data model for Instructor DB table.
    """

    __tablename__ = "instructor"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    school_id = db.Column(db.BIGINT, nullable=True, index=True)
    college_id = db.Column(db.BIGINT, nullable=False, index=True)
    instructor_role_id = db.Column(db.BIGINT, nullable=False, index=True)
    did = db.Column(db.String, nullable=True)
    reference_uri = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "school_id": self.school_id,
            "college_id": self.college_id,
            "instructor_role_id": self.instructor_role_id,
            "did": self.did,
            "reference_uri": self.reference_uri,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return InstructorModel(
            uuid=self.uuid,
            name=self.name,
            school_id=self.school_id,
            college_id=self.college_id,
            instructor_role_id=self.instructor_role_id,
            did=self.did,
            reference_uri=self.reference_uri,
            type=self.type,
            external_id=self.external_id,
        )
