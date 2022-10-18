import logging
import os

import requests

from app.model.credential_schema_tables_model.course_model import CourseModel
from app.persistence.credential_schema_tables_persistence.course_persistence import CoursePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class CourseService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        external_id,
        subject_code,
        catalog_code,
        reference_uri,
        college_id,
        school_id,
        name,
        description,
        credit_hours,
        course_level_id,
        general_ed_id_required,
        general_ed_id_credit,
        program_id_required,
        program_id_credit,
        type,
        credential_type_id,
        parent_organization,
        key,
    ):

        course = CourseModel(
            external_id=external_id,
            subject_code=subject_code,
            catalog_code=catalog_code,
            reference_uri=reference_uri,
            college_id=college_id,
            school_id=school_id,
            name=name,
            description=description,
            credit_hours=credit_hours,
            course_level_id=course_level_id,
            general_ed_id_required=general_ed_id_required,
            general_ed_id_credit=general_ed_id_credit,
            program_id_required=program_id_required,
            program_id_credit=program_id_credit,
            type=type,
            credential_type_id=credential_type_id,
            parent_organization=parent_organization,
            key=key,
        )
        course = CoursePersistence.add(user_id, user_name, course)
        return course

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        course = CoursePersistence.get(uuid)

        if course is None:
            raise RecordNotFound("'course' with uuid '{}' not found.".format(uuid))

        course = CourseModel(
            uuid=uuid,
            external_id=args.get("external_id", course.external_id),
            subject_code=args.get("subject_code", course.subject_code),
            catalog_code=args.get("catalog_code", course.catalog_code),
            reference_uri=args.get("reference_uri", course.reference_uri),
            college_id=args.get("college_id", course.college_id),
            school_id=args.get("school_id", course.school_id),
            name=args.get("name", course.name),
            description=args.get("description", course.description),
            credit_hours=args.get("credit_hours", course.credit_hours),
            course_level_id=args.get("course_level_id", course.course_level_id),
            general_ed_id_required=args.get("general_ed_id_required", course.general_ed_id_required),
            general_ed_id_credit=args.get("general_ed_id_credit", course.general_ed_id_credit),
            program_id_required=args.get("program_id_required", course.program_id_required),
            program_id_credit=args.get("program_id_credit", course.program_id_credit),
            type=args.get("type", course.type),
            credential_type_id=args.get("credential_type_id", course.credential_type_id),
            parent_organization=args.get("parent_organization", course.parent_organization),
            key=args.get("key", course.key),
        )
        course = CoursePersistence.update(user_id, user_name, course)

        return course

    @classmethod
    def delete_all(cls):
        CoursePersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        course = CoursePersistence.get(uuid)
        if course is None:
            raise RecordNotFound("'course' with uuid '{}' not found.".format(uuid))
        CoursePersistence.delete(user_id, user_name, course)
        return course

    @classmethod
    def get(cls, uuid):
        course = CoursePersistence.get(uuid)
        if course is None:
            raise RecordNotFound("'course' with uuid '{}' not found.".format(uuid))
        return course

    @classmethod
    def get_all(cls):
        return CoursePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CoursePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = CoursePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "course", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
