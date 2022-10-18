import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.openbadges_model.badge_model import BadgeModel

_log = logging.getLogger(__name__)


class IssueOpenBadgesBadge:
    @classmethod
    def issue_openbadges_badge(cls, external_id: str, openbadges_badge_schema: BadgeModel):

        _log.info(openbadges_badge_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/openbadges/Badge.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": openbadges_badge_schema.to_dict(),
            "metadata": {},
            "type": "OpenBadgesBadgeCredential",
        }
        openbadges_badge_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {openbadges_badge_response.text}")
        if openbadges_badge_response.status_code == 200:
            return True
        return False
