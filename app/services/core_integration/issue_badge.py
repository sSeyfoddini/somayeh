import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.badge_model import BadgeModel

_log = logging.getLogger(__name__)


class IssueBadge:
    @classmethod
    def issue_badge(cls, external_id: str, badge_schema: BadgeModel):
        print(f"Issuing Badge with external_id: {external_id}")
        _log.info(f"Issuing Badge with external_id: {external_id}")
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Badge.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": badge_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        badge_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {badge_response.text}")
        if badge_response.status_code == 200:
            return True
        return False
