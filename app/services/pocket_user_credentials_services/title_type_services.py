import logging
import os

import requests

from app.model.pocket_user_credentials_model.title_type_model import TitleTypeModel
from app.persistence.pocket_user_credentials_persistence.title_type_persistence import TitleTypePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class TitleTypeService:
    @classmethod
    def add(cls, user_id, user_name, name, description, reference_url, type, external_id):

        title_type = TitleTypeModel(
            name=name,
            description=description,
            reference_url=reference_url,
            type=type,
            external_id=external_id,
        )
        title_type = TitleTypePersistence.add(user_id, user_name, title_type)
        return title_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        title_type = TitleTypePersistence.get(uuid)

        if title_type is None:
            raise RecordNotFound("'title type' with uuid '{}' not found.".format(uuid))

        title_type = TitleTypeModel(
            uuid=uuid,
            name=args.get("name", title_type.name),
            description=args.get("description", title_type.description),
            reference_url=args.get("reference_url", title_type.reference_url),
            type=args.get("type", title_type.type),
            external_id=args.get("external_id", title_type.external_id)
        )
        title_type = TitleTypePersistence.update(user_id, user_name, title_type)

        return title_type

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        title_type = TitleTypePersistence.get(uuid)
        if title_type is None:
            raise RecordNotFound("'title type' with uuid '{}' not found.".format(uuid))
        TitleTypePersistence.delete(user_id, user_name, title_type)
        return title_type

    @classmethod
    def get(cls, uuid):
        title_type = TitleTypePersistence.get(uuid)
        if title_type is None:
            raise RecordNotFound("'title type' with uuid '{}' not found.".format(uuid))
        return title_type

    @classmethod
    def get_all(cls):
        return TitleTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return TitleTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = TitleTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "tytle_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
