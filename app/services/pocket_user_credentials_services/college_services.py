import logging
import os

import requests

from app.model.pocket_user_credentials_model.college_model import CollegeModel
from app.persistence.pocket_user_credentials_persistence.college_persistence import CollegePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class CollegeService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        college_id,
        college_label,
        date,
        type,
        external_id,
        parent_organization,
    ):

        college = CollegeModel(
            credential_type_id=credential_type_id,
            college_id=college_id,
            college_label=college_label,
            date=date,
            type=type,
            external_id=external_id,
            parent_organization=parent_organization,
        )
        college = CollegePersistence.add(user_id, user_name, college)
        return college

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        college = CollegePersistence.get(uuid)

        if college is None:
            raise RecordNotFound("'college' with uuid '{}' not found.".format(uuid))

        college = CollegeModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", college.credential_type_id),
            college_id=args.get("college_id", college.college_id),
            college_label=args.get("college_label", college.college_label),
            date=args.get("date", college.date),
            type=args.get("type", college.type),
            external_id=args.get("external_id", college.external_id),
            parent_organization=args.get("parent_organization", college.parent_organization)
        )
        college = CollegePersistence.update(user_id, user_name, college)

        return college

    @classmethod
    def delete_all(cls):
        CollegePersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        college = CollegePersistence.get(uuid)
        if college is None:
            raise RecordNotFound("'college' with uuid '{}' not found.".format(uuid))
        CollegePersistence.delete(user_id, user_name, college)
        return college

    @classmethod
    def get(cls, uuid):
        college = CollegePersistence.get(uuid)
        if college is None:
            raise RecordNotFound("'college' with uuid '{}' not found.".format(uuid))
        return college

    @classmethod
    def get_all(cls):
        return CollegePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CollegePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = CollegePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "college", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
