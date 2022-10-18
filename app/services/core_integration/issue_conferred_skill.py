import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.conferred_skill_model import ConferredSkillModel

_log = logging.getLogger(__name__)


class ConferredSkillAward:
    @classmethod
    def issue_conferred_skill(cls, external_id: str, conferred_skill_schema: ConferredSkillModel):
        _log.info(conferred_skill_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ConferredSkill.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": conferred_skill_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        conferred_skill_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {conferred_skill_response.text}")
        if conferred_skill_response.status_code == 200:
            return True
        return False
