from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class CourseModel(db.Model):
    """
    Data model for Course DB table.
    """

    __tablename__ = "course"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    external_id = db.Column(db.String, nullable=False)
    subject_code = db.Column(db.String, nullable=False)
    catalog_code = db.Column(db.String, nullable=True)
    reference_uri = db.Column(db.String, nullable=True)
    college_id = db.Column(db.String, nullable=True, index=True)
    school_id = db.Column(db.BIGINT, nullable=True, index=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    credit_hours = db.Column(db.Float, nullable=True)
    course_level_id = db.Column(db.BIGINT, nullable=True, index=True)
    general_ed_id_required = db.Column(db.BIGINT, nullable=True, index=True)
    general_ed_id_credit = db.Column(db.String, nullable=True, index=True)
    program_id_required = db.Column(db.String, nullable=True)
    program_id_credit = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    credential_type_id = db.Column(db.String, nullable=True)
    parent_organization = db.Column(db.String, nullable=True)
    key = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "external_id": self.external_id,
            "subject_code": self.subject_code,
            "catalog_code": self.catalog_code,
            "reference_uri": self.reference_uri,
            "college_id": self.college_id,
            "school_id": self.school_id,
            "name": self.name,
            "description": self.description,
            "credit_hours": self.credit_hours,
            "course_level_id": self.course_level_id,
            "general_ed_id_required": self.general_ed_id_required,
            "general_ed_id_credit": self.general_ed_id_credit,
            "program_id_required": self.program_id_required,
            "program_id_credit": self.program_id_credit,
            "type": self.type,
            "credential_type_id": self.credential_type_id,
            "parent_organization": self.parent_organization,
            "key": self.key,
        }

    def _clone(self):
        return CourseModel(
            uuid=self.uuid,
            external_id=self.external_id,
            subject_code=self.subject_code,
            catalog_code=self.catalog_code,
            reference_uri=self.reference_uri,
            college_id=self.college_id,
            school_id=self.school_id,
            name=self.name,
            description=self.description,
            credit_hours=self.credit_hours,
            course_level_id=self.course_level_id,
            general_ed_id_required=self.general_ed_id_required,
            general_ed_id_credit=self.general_ed_id_credit,
            program_id_required=self.program_id_required,
            program_id_credit=self.program_id_credit,
            type=self.type,
            credential_type_id=self.credential_type_id,
            parent_organization=self.parent_organization,
            key=self.key,
        )
