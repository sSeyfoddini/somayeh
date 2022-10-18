import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.score_model import ScoreModel

_log = logging.getLogger(__name__)


class IssueScore:
    @classmethod
    def issue_score(cls, external_id: str, score_schema: ScoreModel):
        _log.info(score_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Score.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": score_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        score_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {score_response.text}")
        if score_response.status_code == 200:
            return True
        return False
