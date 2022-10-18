import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.award_model import AwardModel

_log = logging.getLogger(__name__)


class IssueAward:
    @classmethod
    def issue_award(cls, external_id: str, award_schema: AwardModel):
        _log.info(award_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Award.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": award_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        award_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {award_response.text}")
        if award_response.status_code == 200:
            return True
        return False
