import uuid

import requests

from app.model.definitions_model.skill_definitions_model import SkillDefinitionsModel
from app.persistence.definitions_persistence.skill_definitions_persistence import SkillDefinitionsPersistence
from app.util.param_keys import ParamKeys
from app.util.param_util import get_param
from app.util.error_handlers import RecordNotFound


class SkillDefinitionsService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        external_id,
        name,
        description,
        category,
        reference_url,
        keywords,
        course_code,
        occupation_ids,
        employer_ids,
    ):

        skill_definitions = SkillDefinitionsModel(
            external_id=external_id,
            name=name,
            description=description,
            category=category,
            reference_url=reference_url,
            keywords=keywords,
            course_code=course_code,
            occupation_ids=occupation_ids,
            employer_ids=employer_ids,
        )
        skill_definitions = SkillDefinitionsPersistence.add(user_id, user_name, skill_definitions)
        return skill_definitions

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        skill_definitions = SkillDefinitionsPersistence.get(uuid)

        if skill_definitions is None:
            raise RecordNotFound("'skill definitions' with uuid'{}' not found.".format(uuid))

        skill_definitions = SkillDefinitionsModel(
            uuid=uuid,
            external_id=args.get("external_id", skill_definitions.external_id),
            name=args.get("name",skill_definitions.name),
            description=args.get("description", skill_definitions.description),
            category=args.get("category", skill_definitions.category),
            reference_url=args.get("reference_url", skill_definitions.reference_url),
            keywords=args.get("keywords", skill_definitions.keywords),
            course_code=args.get("course_code", skill_definitions.course_code),
            occupation_ids=args.get("occupation_ids", skill_definitions.occupation_ids),
            employer_ids=args.get("employer_ids",skill_definitions.employer_ids),
        )
        skill_definitions = SkillDefinitionsPersistence.update(user_id, user_name, skill_definitions)

        return skill_definitions

    @classmethod
    def delete(cls, user_id, user_name, skill_definitions):
        SkillDefinitionsPersistence.delete(user_id, user_name, skill_definitions)
        return skill_definitions

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        skill_definitions = SkillDefinitionsPersistence.get(uuid)
        if skill_definitions is None:
            raise RecordNotFound("'skill definitions' with uuid'{}' not found.".format(uuid))
        SkillDefinitionsPersistence.delete(user_id, user_name, skill_definitions)
        return skill_definitions

    @classmethod
    def get(cls, uuid):
        skill_definitions = SkillDefinitionsPersistence.get(uuid)
        if skill_definitions is None:
            raise RecordNotFound("'skill definitions' with uuid'{}' not found.".format(uuid))
        return skill_definitions

    @classmethod
    def get_all(cls):
        return SkillDefinitionsPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return SkillDefinitionsPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue_skill(cls, external_id: str):
        pocket_core_api_credential = get_param(ParamKeys.POCKET_CORE_BASE_URL) + "/credential/issue"

        skills = SkillDefinitionsPersistence.get_all()
        for skill in skills:
            PARAMS = {
                "external_connection_id": external_id,
                "external_schema_id": "skill",
                "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
                "comment": "",
                "attributes": skill._to_dict,
            }
            requests.post(pocket_core_api_credential, json=PARAMS)
