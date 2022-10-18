import logging
import os

import requests

from app.model.credential_schema_tables_model.general_education_model import GeneralEducationModel
from app.persistence.credential_schema_tables_persistence.general_education_persistence import (
    GeneralEducationPersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class GeneralEducationService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        abbreviation,
        description,
        label,
        college_id,
        reference_uri,
        type,
        external_id,
    ):

        general_education = GeneralEducationModel(
            name=name,
            abbreviation=abbreviation,
            description=description,
            label=label,
            college_id=college_id,
            reference_uri=reference_uri,
            type=type,
            external_id=external_id,
        )
        general_education = GeneralEducationPersistence.add(user_id, user_name, general_education)
        return general_education

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        general_education = GeneralEducationPersistence.get(uuid)

        if general_education is None:
            raise RecordNotFound("'general education' with uuid '{}' not found.".format(uuid))

        general_education = GeneralEducationModel(
            uuid=uuid,
            name=args.get("name", general_education.name),
            abbreviation=args.get("abbreviation", general_education.abbreviation),
            description=args.get("description", general_education.description),
            label=args.get("label", general_education.label),
            college_id=args.get("college_id", general_education.college_id),
            reference_uri=args.get("reference_uri", general_education.reference_uri),
            type=args.get("type", general_education.type),
            external_id=args.get("external_id", general_education.external_id)
        )
        general_education = GeneralEducationPersistence.update(user_id, user_name, general_education)

        return general_education

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        general_education = GeneralEducationPersistence.get(uuid)
        if general_education is None:
            raise RecordNotFound("'general education' with uuid '{}' not found.".format(uuid))
        GeneralEducationPersistence.delete(user_id, user_name, general_education)
        return general_education

    @classmethod
    def get(cls, uuid):
        general_education = GeneralEducationPersistence.get(uuid)
        if general_education is None:
            raise RecordNotFound("'general education' with uuid '{}' not found.".format(uuid))
        return general_education

    @classmethod
    def get_all(cls):
        return GeneralEducationPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return GeneralEducationPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = GeneralEducationPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "general_education", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
