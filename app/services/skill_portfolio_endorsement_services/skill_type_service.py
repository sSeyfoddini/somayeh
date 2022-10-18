import logging
import os

import requests

from app.model.skill_portfolio_endorsement_model.skill_type_model import SkillTypeModel
from app.persistence.skill_portfolio_endorsement_persistence.skill_type_persistence import SkillTypePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class SkillTypeService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        description,
        category_id,
        category_name,
        Updates_for_POCKMMVP_1030,
        reference_url,
        source_skill_type_id,
        occupation_ids,
        employer_ids,
        keywords,
        rsd,
        rsd_uri,
    ):

        skill_type = SkillTypeModel(
            name=name,
            description=description,
            category_id=str(category_id),
            category_name=str(category_name),
            Updates_for_POCKMMVP_1030=Updates_for_POCKMMVP_1030,
            reference_url=reference_url,
            source_skill_type_id=source_skill_type_id,
            occupation_ids=occupation_ids,
            employer_ids=employer_ids,
            keywords=str(keywords),
            rsd=rsd,
            rsd_uri=rsd_uri,
        )
        skill_type = SkillTypePersistence.add(user_id, user_name, skill_type)
        return skill_type

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        skill_type = SkillTypePersistence.get(uuid)

        if skill_type is None:
            raise RecordNotFound("'skill type' with uuid '{}' not found.".format(uuid))

        skill_type = SkillTypeModel(
            uuid=uuid,
            name=args.get("name", skill_type.name),
            description=args.get("description", skill_type.description),
            category_id=args.get("category_id", skill_type.category_id),
            category_name=args.get("category_name", skill_type.category_name),
            Updates_for_POCKMMVP_1030=args.get("Updates_for_POCKMMVP_1030", skill_type.Updates_for_POCKMMVP_1030),
            reference_url=args.get("reference_url", skill_type.reference_url),
            source_skill_type_id=args.get("source_skill_type_id", skill_type.source_skill_type_id),
            occupation_ids=args.get("occupation_ids", skill_type.occupation_ids),
            employer_ids=args.get("employer_ids", skill_type.employer_ids),
            keywords=args.get("keywords", skill_type.keywords),
            rsd=args.get("rsd", skill_type.rsd),
            rsd_uri=args.get("rsd_uri", skill_type.rsd_uri),
        )
        skill_type = SkillTypePersistence.update(user_id, user_name, skill_type)

        return skill_type

    @classmethod
    def delete_all(cls):
        SkillTypePersistence.delete_all()

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        skill_type = SkillTypePersistence.get(uuid)
        if skill_type is None:
            raise RecordNotFound("'skill type' with uuid '{}' not found.".format(uuid))
        SkillTypePersistence.delete(user_id, user_name, skill_type)
        return skill_type

    @classmethod
    def get(cls, uuid):
        skill_type = SkillTypePersistence.get(uuid)
        if skill_type is None:
            raise RecordNotFound("'skill type' with uuid '{}' not found.".format(uuid))
        return skill_type

    @classmethod
    def get_all(cls):
        return SkillTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return SkillTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = SkillTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "skill_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)

    @classmethod
    def get_by_reference_url(cls, reference_url: str):
        result = SkillTypePersistence.get_by_reference_url(reference_url)
        return result
