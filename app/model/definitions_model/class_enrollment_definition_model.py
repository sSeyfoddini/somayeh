from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class ClassEnrollmentDefinitionModel(db.Model):
    """
    Data model for class enrollment Definition DB table.
    """

    __tablename__ = "class_enrollment_definition"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    course_id = db.Column(db.BIGINT, nullable=False)
    course_subject = db.Column(db.String, nullable=False)
    course_number = db.Column(db.String, nullable=False)
    course_name = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "course_id": self.course_id,
            "course_subject": self.course_subject,
            "course_number": self.course_number,
            "course_name": self.course_name,
        }

    def _clone(self):
        return ClassEnrollmentDefinitionModel(
            uuid=self.uuid,
            course_id=self.course_id,
            course_subject=self.course_subject,
            course_number=self.course_number,
            course_name=self.course_name,
        )
