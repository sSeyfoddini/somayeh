import logging
import os

import requests

from app.model.skill_portfolio_endorsement_model.source_skill_library_model import SourceSkillLibraryModel
from app.persistence.skill_portfolio_endorsement_persistence.source_skill_library_persistence import (
    SourceSkillLibraryPersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class SourceSkillLibraryService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        description,
        external_id,
        reference_uri,
        type,
    ):

        source_skill_library = SourceSkillLibraryModel(
            name=name,
            description=description,
            external_id=external_id,
            reference_uri=reference_uri,
            type=type,
        )
        source_skill_library = SourceSkillLibraryPersistence.add(user_id, user_name, source_skill_library)
        return source_skill_library

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        source_skill_library = SourceSkillLibraryPersistence.get(uuid)

        if source_skill_library is None:
            raise RecordNotFound("'skill type' with uuid '{}' not found.".format(uuid))

        source_skill_library = SourceSkillLibraryModel(
            uuid=uuid,
            name=args.get("name", source_skill_library.name),
            description=args.get("description", source_skill_library.description),
            external_id=args.get("external_id", source_skill_library.external_id),
            reference_uri=args.get("reference_uri", source_skill_library.reference_uri),
            type=args.get("type", source_skill_library.type)
        )
        source_skill_library = SourceSkillLibraryPersistence.update(user_id, user_name, source_skill_library)

        return source_skill_library

    @classmethod
    def delete(cls, user_id, user_name, source_skill_library):
        SourceSkillLibraryPersistence.delete(user_id, user_name, source_skill_library)
        return source_skill_library

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        source_skill_library = SourceSkillLibraryPersistence.get(uuid)
        if source_skill_library is None:
            raise RecordNotFound("'skill type' with uuid '{}' not found.".format(uuid))
        SourceSkillLibraryPersistence.delete(user_id, user_name, source_skill_library)
        return source_skill_library

    @classmethod
    def get(cls, uuid):
        source_skill_library = SourceSkillLibraryPersistence.get(uuid)
        if source_skill_library is None:
            raise RecordNotFound("'skill type' with uuid '{}' not found.".format(uuid))
        return source_skill_library

    @classmethod
    def get_all(cls):
        return SourceSkillLibraryPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return SourceSkillLibraryPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = SourceSkillLibraryPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "source_skill_library", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
