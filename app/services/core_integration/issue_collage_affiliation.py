import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.collage_affiliation_model import CollageAffiliationModel

_log = logging.getLogger(__name__)


class IssueCollageAffiliation:
    @classmethod
    def issue_collage_affiliation(cls, external_id: str, collage_affiliation_schema: CollageAffiliationModel):
        _log.info(collage_affiliation_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/CollageAffiliation.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": collage_affiliation_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        collage_affiliation_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {collage_affiliation_response.text}")
        if collage_affiliation_response.status_code == 200:
            return True
        return False
