import logging
import os

import requests

from app.model.pocket_user_credentials_model.school_model import SchoolModel
from app.persistence.pocket_user_credentials_persistence.school_persistence import SchoolPersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class SchoolService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        school_id,
        school_label,
        date,
        type,
        external_id,
        parent_organization
    ):

        school = SchoolModel(
            credential_type_id=credential_type_id,
            school_id=school_id,
            school_label=school_label,
            date=date,
            type=type,
            external_id=external_id,
            parent_organization=parent_organization
        )
        school = SchoolPersistence.add(user_id, user_name, school)
        return school

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        school = SchoolPersistence.get(uuid)

        if school is None:
            raise RecordNotFound("'school' with uuid '{}' not found.".format(uuid))

        school = SchoolModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", school.credential_type_id),
            school_id=args.get("school_id", school.school_id),
            school_label=args.get("school_label", school.school_label),
            date=args.get("date", school.date),
            type=args.get("type", school.type),
            external_id=args.get("external_id", school.external_id),
            parent_organization=args.get("parent_organization", school.parent_organization)
        )
        school = SchoolPersistence.update(user_id, user_name, school)

        return school

    @classmethod
    def delete_all(cls):
        SchoolPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        school = SchoolPersistence.get(uuid)
        if school is None:
            raise RecordNotFound("'school' with uuid '{}' not found.".format(uuid))
        SchoolPersistence.delete(user_id, user_name, school)
        return school

    @classmethod
    def get(cls, uuid):
        school = SchoolPersistence.get(uuid)
        if school is None:
            raise RecordNotFound("'school' with uuid '{}' not found.".format(uuid))
        return school

    @classmethod
    def get_all(cls):
        return SchoolPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return SchoolPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = SchoolPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "school", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
