import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.class_incomplete_model import ClassIncompleteModel

_log = logging.getLogger(__name__)


class IssueClassIncomplete:
    @classmethod
    def issue_class_incomplete(cls, external_id: str, class_incomplete_schema: ClassIncompleteModel):
        _log.info(class_incomplete_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ClassIncomplete.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": class_incomplete_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        class_incomplete_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {class_incomplete_response.text}")
        if class_incomplete_response.status_code == 200:
            return True
        return False
