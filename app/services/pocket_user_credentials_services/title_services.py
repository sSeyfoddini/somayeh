import logging
import os

import requests

from app.model.pocket_user_credentials_model.title_model import TitleModel
from app.persistence.pocket_user_credentials_persistence.title_persistence import TitlePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class TitleService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        credential_type_label,
        title_type_id,
        title_type_label,
        organization_id,
        organization_label,
        conferral_date,
        type,
        external_id,
    ):

        title = TitleModel(
            credential_type_id=credential_type_id,
            credential_type_label=credential_type_label,
            title_type_id=title_type_id,
            title_type_label=title_type_label,
            organization_id=organization_id,
            organization_label=organization_label,
            conferral_date=conferral_date,
            type=type,
            external_id=external_id,
        )
        title = TitlePersistence.add(user_id, user_name, title)
        return title

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        title = TitlePersistence.get(uuid)

        if title is None:
            raise RecordNotFound("'title' with uuid '{}' not found.".format(uuid))

        title = TitleModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", title.credential_type_id),
            credential_type_label=args.get("credential_type_label", title.credential_type_label),
            title_type_id=args.get("title_type_id", title.title_type_id),
            title_type_label=args.get("title_type_label", title.title_type_label),
            organization_id=args.get("organization_id", title.organization_id),
            organization_label=args.get("organization_label", title.organization_label),
            conferral_date=args.get("conferral_date", title.conferral_date),
            type=args.get("type", title.type),
            external_id=args.get("external_id", title.external_id)
        )
        title = TitlePersistence.update(user_id, user_name, title)

        return title

    @classmethod
    def delete_all(cls):
        TitlePersistence.delete_all()

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        title = TitlePersistence.get(uuid)
        if title is None:
            raise RecordNotFound("'title' with uuid '{}' not found.".format(uuid))
        TitlePersistence.delete(user_id, user_name, title)
        return title

    @classmethod
    def get(cls, uuid):
        title = TitlePersistence.get(uuid)
        if title is None:
            raise RecordNotFound("'title' with uuid '{}' not found.".format(uuid))
        return title

    @classmethod
    def get_all(cls):
        return TitlePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return TitlePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = TitlePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "title", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
