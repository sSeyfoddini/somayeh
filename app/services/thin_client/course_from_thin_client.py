
from app import db
from app.model.credential_schema_tables_model.course_model import CourseModel
from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.persistence.credential_schema_tables_persistence.course_persistence import CoursePersistence
from app.services.thin_client_service import CourseService

class Course:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"
        page = 1
        body = {
            "crse_id": "108064",
            "crs_topic_id": 109
        }

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid).filter(CredentialTypeModel.name == "course").scalar()
        )

        while True:
            response = CourseService.get(page, limit, body)
            if not response:
                break
            page = page + 1
            for data in response:
                old_course = CoursePersistence.get_by_external_user_id(data["crse_id"])
                if old_course:
                    # update table
                    old_course = old_course[0]
                    course = CourseModel(
                        uuid=old_course.uuid,
                        external_id=old_course.external_id,
                        subject_code=old_course.subject_code,
                        catalog_code=old_course.catalog_code,
                        reference_uri=old_course.reference_uri,
                        college_id=old_course.college_id,
                        school_id=old_course.school_id,
                        name=old_course.name,
                        description=data["descr"],
                        credit_hours=old_course.credit_hours,
                        course_level_id=old_course.course_level_id,
                        general_ed_id_required=old_course.general_ed_id_required,
                        general_ed_id_credit=old_course.general_ed_id_credit,
                        program_id_required=old_course.program_id_required,
                        program_id_credit=old_course.program_id_credit,
                        type=old_course.type,
                        credential_type_id=credential_type_id,
                        parent_organization=parent_organization,
                        key=old_course.key

                    )
                    CoursePersistence.update(user_id, user_name, course)
                else:
                    # insert in table
                    course = CourseModel(
                        external_id=data["crse_id"],
                        subject_code="",
                        catalog_code="",
                        reference_uri="",
                        college_id=None,
                        school_id=None,
                        name="",
                        description=data["descr"],
                        credit_hours=None,
                        course_level_id=None,
                        general_ed_id_required=None,
                        general_ed_id_credit="",
                        program_id_required="",
                        program_id_credit="",
                        type="",
                        credential_type_id=credential_type_id,
                        parent_organization=parent_organization,
                        key="",
                    )
                    CoursePersistence.add(user_id, user_name, course)
