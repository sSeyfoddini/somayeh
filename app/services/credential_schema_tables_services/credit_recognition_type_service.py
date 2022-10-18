import logging
import os

import requests

from app.model.credential_schema_tables_model.credit_recognition_type_model import CreditRecognitionTypeModel
from app.persistence.credential_schema_tables_persistence.credit_recognition_type_persistence import (
    CreditRecognitionTypePersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class CreditRecognitionTypeService:
    @classmethod
    def add(cls, user_id, user_name, name, description, type, external_id):

        credit_recognition_type = CreditRecognitionTypeModel(
            name=name, description=description, type=type, external_id=external_id
        )
        credit_recognition_type = CreditRecognitionTypePersistence.add(user_id, user_name, credit_recognition_type)
        return credit_recognition_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        credit_recognition_type = CreditRecognitionTypePersistence.get(uuid)

        if credit_recognition_type is None:
            raise RecordNotFound("'credit recognition type' with uuid '{}' not found.".format(uuid))

        credit_recognition_type = CreditRecognitionTypeModel(
            uuid=uuid,
            name=args.get("name", credit_recognition_type.name),
            description=args.get("description", credit_recognition_type.description),
            type=args.get("type", credit_recognition_type.type),
            external_id=args.get("external_id", credit_recognition_type.external_id),
        )
        credit_recognition_type = CreditRecognitionTypePersistence.update(user_id, user_name, credit_recognition_type)

        return credit_recognition_type

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        credit_recognition_type = CreditRecognitionTypePersistence.get(uuid)
        if credit_recognition_type is None:
            raise RecordNotFound("'credit recognition type' with uuid '{}' not found.".format(uuid))
        CreditRecognitionTypePersistence.delete(user_id, user_name, credit_recognition_type)
        return credit_recognition_type

    @classmethod
    def get(cls, uuid):
        credit_recognition_type = CreditRecognitionTypePersistence.get(uuid)
        if credit_recognition_type is None:
            raise RecordNotFound("'credit recognition type' with uuid '{}' not found.".format(uuid))
        return credit_recognition_type

    @classmethod
    def get_all(cls):
        return CreditRecognitionTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CreditRecognitionTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = CreditRecognitionTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "credit_recognition_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
