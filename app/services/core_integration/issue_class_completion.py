import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.class_completion_model import ClassCompletionModel

_log = logging.getLogger(__name__)


class IssueClassCompletion:
    @classmethod
    def issue_class_completion(cls, external_id: str, class_completion_schema: ClassCompletionModel):
        _log.info(class_completion_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ClassCompletion.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": class_completion_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        class_completion_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {class_completion_response.text}")
        if class_completion_response.status_code == 200:
            return True
        return False
