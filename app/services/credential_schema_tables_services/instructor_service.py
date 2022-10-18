
import logging
import os

import requests

from app.model.credential_schema_tables_model.instructor_model import InstructorModel
from app.persistence.credential_schema_tables_persistence.instructor_persistence import InstructorPersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class InstructorService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        school_id,
        college_id,
        instructor_role_id,
        did,
        reference_uri,
        type,
        external_id,
    ):

        instructor = InstructorModel(
            name=name,
            school_id=school_id,
            college_id=college_id,
            instructor_role_id=instructor_role_id,
            did=did,
            reference_uri=reference_uri,
            type=type,
            external_id=external_id,
        )
        instructor = InstructorPersistence.add(user_id, user_name, instructor)
        return instructor

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        instructor = InstructorPersistence.get(uuid)

        if instructor is None:
            raise RecordNotFound("'instructor' with uuid '{}' not found.".format(uuid))

        instructor = InstructorModel(
            uuid=uuid,
            name=args.get("name", instructor.name),
            school_id=args.get("school_id", instructor.school_id),
            college_id=args.get("college_id", instructor.college_id),
            instructor_role_id=args.get("instructor_role_id", instructor.instructor_role_id),
            did=args.get("did", instructor.did),
            reference_uri=args.get("reference_uri", instructor.reference_uri),
            type=args.get("type", instructor.type),
            external_id=args.get("external_id", instructor.external_id)
        )
        instructor = InstructorPersistence.update(user_id, user_name, instructor)

        return instructor


    @classmethod
    def delete(cls, user_id, user_name, uuid):
        instructor = InstructorPersistence.get(uuid)
        if instructor is None:
            raise RecordNotFound("'instructor' with uuid '{}' not found.".format(uuid))
        InstructorPersistence.delete(user_id, user_name, instructor)
        return instructor

    @classmethod
    def get(cls, uuid):
        instructor = InstructorPersistence.get(uuid)
        if instructor is None:
            raise RecordNotFound("'instructor' with uuid '{}' not found.".format(uuid))
        return instructor

    @classmethod
    def get_all(cls):
        return InstructorPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return InstructorPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = InstructorPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "instructor", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
