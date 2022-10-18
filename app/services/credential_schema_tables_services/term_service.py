import logging
import os

import requests

from app.model.credential_schema_tables_model.term_model import TermModel
from app.persistence.credential_schema_tables_persistence.term_persistence import TermPersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class TermService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        start_date,
        end_date,
        session_id,
        type,
        external_id,
        credential_type_id,
        parent_organization,
    ):

        term = TermModel(
            name=name,
            start_date=start_date,
            end_date=end_date,
            session_id=session_id,
            type=type,
            external_id=external_id,
            credential_type_id=credential_type_id,
            parent_organization=parent_organization,
        )
        term = TermPersistence.add(user_id, user_name, term)
        return term

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        term = TermPersistence.get(uuid)

        if term is None:
            raise RecordNotFound("'term' with uuid '{}' not found.".format(uuid))

        term = TermModel(
            uuid=uuid,
            name=args.get("name", term.name),
            start_date=args.get("start_date", term.start_date),
            end_date=args.get("end_date", term.end_date),
            session_id=args.get("session_id", term.session_id),
            type=args.get("type", term.type),
            external_id=args.get("external_id", term.external_id),
            credential_type_id=args.get("credential_type_id", term.credential_type_id),
            parent_organization=args.get("parent_organization", term.parent_organization)
        )
        term = TermPersistence.update(user_id, user_name, term)

        return term

    @classmethod
    def delete_all(cls):
        TermPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        term = TermPersistence.get(uuid)
        if term is None:
            raise RecordNotFound("'term' with uuid '{}' not found.".format(uuid))
        TermPersistence.delete(user_id, user_name, term)
        return term

    @classmethod
    def get(cls, uuid):
        term = TermPersistence.get(uuid)
        if term is None:
            raise RecordNotFound("'term' with uuid '{}' not found.".format(uuid))
        return term

    @classmethod
    def get_all(cls):
        return TermPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return TermPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = TermPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "term", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
