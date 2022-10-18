import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.openbadges_model.image_model import ImageModel

_log = logging.getLogger(__name__)


class IssueOpenBadgesImage:
    @classmethod
    def issue_openbadges_image(cls, external_id: str, openbadges_image_schema: ImageModel):
        _log.info(openbadges_image_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/openbadges/image.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": openbadges_image_schema.to_dict(),
            "metadata": {},
            "type": "OpenBadgesimageCredential",
        }
        openbadges_image_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {openbadges_image_response.text}")
        if openbadges_image_response.status_code == 200:
            return True
        return False
