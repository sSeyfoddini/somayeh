import logging
import os

import requests

from app.model.credential_schema_tables_model.general_education_fulfillment_model import (
    GeneralEducationFulfillmentModel,
)
from app.persistence.credential_schema_tables_persistence.general_education_fulfillment_persistence import (
    GeneralEducationFulfillmentPersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class GeneralEducationFulfillmentService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        credential_type_label,
        recognition_date,
        term_id,
        term_label,
        gen_ed_id,
        credential_label,
        gen_ed_name,
        type,
        external_id,
    ):

        general_education_fulfillment = GeneralEducationFulfillmentModel(
            credential_type_id=credential_type_id,
            credential_type_label=credential_type_label,
            recognition_date=recognition_date,
            term_id=term_id,
            term_label=term_label,
            gen_ed_id=gen_ed_id,
            credential_label=credential_label,
            gen_ed_name=gen_ed_name,
            type=type,
            external_id=external_id,
        )
        general_education_fulfillment = GeneralEducationFulfillmentPersistence.add(
            user_id, user_name, general_education_fulfillment
        )
        return general_education_fulfillment

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        general_education_fulfillment = GeneralEducationFulfillmentPersistence.get(uuid)

        if general_education_fulfillment is None:
            raise RecordNotFound("'general education fulfillment' with uuid '{}' not found.".format(uuid))

        general_education_fulfillment = GeneralEducationFulfillmentModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", general_education_fulfillment.credential_type_id),
            credential_type_label=args.get("credential_type_label", general_education_fulfillment.credential_type_label),
            recognition_date=args.get("recognition_date", general_education_fulfillment.recognition_date),
            term_id=args.get("term_id", general_education_fulfillment.term_id),
            term_label=args.get("term_label", general_education_fulfillment.term_label),
            gen_ed_id=args.get("gen_ed_id", general_education_fulfillment.gen_ed_id),
            credential_label=args.get("credential_label", general_education_fulfillment.credential_label),
            gen_ed_name=args.get("gen_ed_name", general_education_fulfillment.gen_ed_name),
            type=args.get("type", general_education_fulfillment.type),
            external_id=args.get("external_id", general_education_fulfillment.external_id),
        )
        general_education_fulfillment = GeneralEducationFulfillmentPersistence.update(
            user_id, user_name, general_education_fulfillment
        )

        return general_education_fulfillment

    @classmethod
    def delete(cls, user_id, user_name, general_education_fulfillment):
        GeneralEducationFulfillmentPersistence.delete(user_id, user_name, general_education_fulfillment)
        return general_education_fulfillment

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        general_education_fulfillment = GeneralEducationFulfillmentPersistence.get(uuid)
        if general_education_fulfillment is None:
            raise RecordNotFound("'general education fulfillment' with uuid '{}' not found.".format(uuid))
        GeneralEducationFulfillmentPersistence.delete(user_id, user_name, general_education_fulfillment)
        return general_education_fulfillment

    @classmethod
    def get(cls, uuid):
        general_education_fulfillment = GeneralEducationFulfillmentPersistence.get(uuid)
        if general_education_fulfillment is None:
            raise RecordNotFound("'general education fulfillment' with uuid '{}' not found.".format(uuid))
        return general_education_fulfillment

    @classmethod
    def get_all(cls):
        return GeneralEducationFulfillmentPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return GeneralEducationFulfillmentPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = GeneralEducationFulfillmentModel.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "general_education_fulfillment", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
