import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.milleston_completion_model import MillestonCompletionModel

_log = logging.getLogger(__name__)


class IssueMillestonCompletion:
    @classmethod
    def issue_milleston_completion(cls, external_id: str, milleston_completion_schema: MillestonCompletionModel):
        _log.info(milleston_completion_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/MillestonCompletion.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": milleston_completion_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        milleston_completion_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {milleston_completion_response.text}")
        if milleston_completion_response.status_code == 200:
            return True
        return False
