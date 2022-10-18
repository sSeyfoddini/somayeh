import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.general_ed_model import GeneralEdModel

_log = logging.getLogger(__name__)


class IssueGeneralEd:
    @classmethod
    def issue_general_ed(cls, external_id: str, general_ed_schema: GeneralEdModel):
        _log.info(general_ed_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/GeneralEd.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": general_ed_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        general_ed_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {general_ed_response.text}")
        if general_ed_response.status_code == 200:
            return True
        return False
