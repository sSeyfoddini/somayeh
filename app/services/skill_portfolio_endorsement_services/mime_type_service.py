import logging
import os

import requests

from app.model.skill_portfolio_endorsement_model.mime_type_model import MimeTypeModel
from app.persistence.skill_portfolio_endorsement_persistence.mime_type_persistence import MimeTypePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class MimeTypeService:
    @classmethod
    def add(cls, user_id, user_name, mime_type1, extension, type, external_id):

        mime_type = MimeTypeModel(
            mime_type1=mime_type1,
            extension=extension,
            type=type,
            external_id=external_id,
        )
        mime_type = MimeTypePersistence.add(user_id, user_name, mime_type)
        return mime_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        mime_type = MimeTypePersistence.get(uuid)

        if mime_type is None:
            raise RecordNotFound("'mime type' with uuid '{}' not found.".format(uuid))

        mime_type = MimeTypeModel(
            uuid=uuid,
            mime_type1=args.get("mime_type1", mime_type.mime_type1),
            extension=args.get("extension", mime_type.extension),
            type=args.get("type", mime_type.type),
            external_id=args.get("external_id", mime_type.external_id),
        )
        mime_type = MimeTypePersistence.update(user_id, user_name, mime_type)

        return mime_type

    @classmethod
    def delete(cls, user_id, user_name, mime_type):
        MimeTypePersistence.delete(user_id, user_name, mime_type)
        return mime_type

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        mime_type = MimeTypePersistence.get(uuid)
        if mime_type is None:
            raise RecordNotFound("'mime type' with uuid '{}' not found.".format(uuid))
        MimeTypePersistence.delete(user_id, user_name, mime_type)
        return mime_type

    @classmethod
    def get(cls, uuid):
        mime_type = MimeTypePersistence.get(uuid)
        if mime_type is None:
            raise RecordNotFound("'mime type' with uuid '{}' not found.".format(uuid))
        return mime_type

    @classmethod
    def get_all(cls):
        return MimeTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return MimeTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = MimeTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "mime_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
