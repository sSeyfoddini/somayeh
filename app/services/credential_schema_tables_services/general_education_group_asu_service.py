import logging
import os

import requests

from app.model.credential_schema_tables_model.general_education_group_asu_model import GeneralEducationGroupASUModel
from app.persistence.credential_schema_tables_persistence.general_education_group_asu_persistence import (
    GeneralEducationGroupASUPersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class GeneralEducationGroupASUService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        description,
        external_id,
        gen_id_list,
        gen_code_list,
        credential_type_id,
        parent_organization,
    ):

        general_education_group_asu = GeneralEducationGroupASUModel(
            name=name,
            description=description,
            external_id=external_id,
            gen_id_list=gen_id_list,
            gen_code_list=gen_code_list,
            credential_type_id=credential_type_id,
            parent_organization=parent_organization
        )
        general_education_group_asu = GeneralEducationGroupASUPersistence.add(
            user_id, user_name, general_education_group_asu
        )
        return general_education_group_asu

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        general_education_group_asu = GeneralEducationGroupASUPersistence.get(uuid)

        if general_education_group_asu is None:
            raise RecordNotFound("'general education fulfillment' with uuid '{}' not found.".format(uuid))

        general_education_group_asu = GeneralEducationGroupASUModel(
            uuid=uuid,
            name=args.get("name", general_education_group_asu.name),
            description=args.get("description", general_education_group_asu.description),
            external_id=args.get("external_id", general_education_group_asu.external_id),
            gen_id_list=args.get("gen_id_list", general_education_group_asu.gen_id_list),
            gen_code_list=args.get("gen_code_list", general_education_group_asu.gen_code_list),
            credential_type_id=args.get("credential_type_id", general_education_group_asu.credential_type_id),
            parent_organization=args.get("parent_organization", general_education_group_asu.parent_organization)
        )
        general_education_group_asu = GeneralEducationGroupASUPersistence.update(
            user_id, user_name, general_education_group_asu
        )

        return general_education_group_asu

    @classmethod
    def delete_all(cls):
        GeneralEducationGroupASUPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        general_education_group_asu = GeneralEducationGroupASUPersistence.get(uuid)
        if general_education_group_asu is None:
            raise RecordNotFound("'general education fulfillment' with uuid '{}' not found.".format(uuid))
        GeneralEducationGroupASUPersistence.delete(user_id, user_name, general_education_group_asu)
        return general_education_group_asu

    @classmethod
    def get(cls, uuid):
        general_education_group_asu = GeneralEducationGroupASUPersistence.get(uuid)
        if general_education_group_asu is None:
            raise RecordNotFound("'general education fulfillment' with uuid '{}' not found.".format(uuid))
        return general_education_group_asu

    @classmethod
    def get_all(cls):
        return GeneralEducationGroupASUPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return GeneralEducationGroupASUPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = GeneralEducationGroupASUPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "general_education_group_asu", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
