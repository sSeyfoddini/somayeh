import logging
import os

import requests

from app.model.skill_portfolio_endorsement_model.source_skill_type_model import SourceSkillTypeModel
from app.persistence.skill_portfolio_endorsement_persistence.source_skill_type_persistence import (
    SourceSkillTypePersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class SourceSkillTypeService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        description,
        source_skill_library_id,
        external_id,
        reference_uri,
        category,
        occupations,
        employer,
        certifications,
        keywords,
        type,
    ):

        source_skill_type = SourceSkillTypeModel(
            name=name,
            description=description,
            source_skill_library_id=source_skill_library_id,
            external_id=external_id,
            reference_uri=reference_uri,
            category=category,
            occupations=occupations,
            employer=employer,
            certifications=certifications,
            keywords=keywords,
            type=type,
        )
        source_skill_type = SourceSkillTypePersistence.add(user_id, user_name, source_skill_type)
        return source_skill_type

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        source_skill_type = SourceSkillTypePersistence.get(uuid)

        if source_skill_type is None:
            raise RecordNotFound("'source skill type' with uuid '{}' not found.".format(uuid))

        source_skill_type = SourceSkillTypeModel(
            uuid=uuid,
            name=args.get("name", source_skill_type.name),
            description=args.get("description", source_skill_type.description),
            source_skill_library_id=args.get("source_skill_library_id", source_skill_type.source_skill_library_id),
            external_id=args.get("external_id", source_skill_type.external_id),
            reference_uri=args.get("reference_uri", source_skill_type.reference_uri),
            category=args.get("category", source_skill_type.category),
            occupations=args.get("occupations", source_skill_type.occupations),
            employer=args.get("employer", source_skill_type.employer),
            certifications=args.get("certifications", source_skill_type.certifications),
            keywords=args.get("keywords", source_skill_type.keywords),
            type=args.get("type", source_skill_type.type)
        )
        source_skill_type = SourceSkillTypePersistence.update(user_id, user_name, source_skill_type)

        return source_skill_type

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        source_skill_type = SourceSkillTypePersistence.get(uuid)
        if source_skill_type is None:
            raise RecordNotFound("'source skill type' with uuid '{}' not found.".format(uuid))
        SourceSkillTypePersistence.delete(user_id, user_name, source_skill_type)
        return source_skill_type

    @classmethod
    def get(cls, uuid):
        source_skill_type = SourceSkillTypePersistence.get(uuid)
        if source_skill_type is None:
            raise RecordNotFound("'source skill type' with uuid '{}' not found.".format(uuid))
        return source_skill_type

    @classmethod
    def get_all(cls):
        return SourceSkillTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return SourceSkillTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = SourceSkillTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "source_skill_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
