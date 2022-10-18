import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.openbadges_model.skill_model import SkillModel

_log = logging.getLogger(__name__)


class IssueOpenBadgesSkill:
    @classmethod
    def issue_skill(cls, external_id: str, openbadges_skill_schema: SkillModel):

        _log.info(openbadges_skill_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/openbadges/Skill.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": openbadges_skill_schema.to_dict(),
            "metadata": {},
            "type": "OpenBadgesSkillCredential",
        }
        openbadges_skill_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {openbadges_skill_response.text}")
        if openbadges_skill_response.status_code == 200:
            return True
        return False
