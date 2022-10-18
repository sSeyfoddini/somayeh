from uuid import uuid4

from app import db

def uuid():
    return str(uuid4())


class ClassModel(db.Model):
    """
    Data model for Class DB table.
    """

    __tablename__ = "class"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    external_class_id = db.Column(db.String, nullable=False)
    course_id = db.Column(db.String, nullable=True)
    external_course_id = db.Column(db.String)
    instructor_id = db.Column(db.BIGINT, nullable=True)
    session_id = db.Column(db.String, nullable=False)
    term_id = db.Column(db.BIGINT, nullable=False)
    topic = db.Column(db.String, nullable=True)
    reference_uri = db.Column(db.String, nullable=True)
    delivery_id = db.Column(db.BIGINT, nullable=True)
    location_id = db.Column(db.BIGINT, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "external_class_id": self.external_class_id,
            "course_id": self.course_id,
            "external_course_id": self.external_course_id,
            "instructor_id": self.instructor_id,
            "session_id": self.session_id,
            "term_id": self.term_id,
            "topic": self.topic,
            "reference_uri": self.reference_uri,
            "delivery_id": self.delivery_id,
            "location_id": self.location_id,
        }

    def _clone(self):
        return ClassModel(
            uuid=self.uuid,
            external_class_id=self.external_class_id,
            course_id=self.course_id,
            external_course_id=self.external_course_id,
            instructor_id=self.instructor_id,
            session_id=self.session_id,
            term_id=self.term_id,
            topic=self.topic,
            reference_uri=self.reference_uri,
            delivery_id=self.delivery_id,
            location_id=self.location_id,
        )
