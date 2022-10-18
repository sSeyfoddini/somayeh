import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.degree_model import DegreeModel

_log = logging.getLogger(__name__)


class IssueDegree:
    @classmethod
    def issue_degree(cls, external_id: str, degree_schema: DegreeModel):
        _log.info(degree_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Degree.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": degree_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        degree_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {degree_response.text}")
        if degree_response.status_code == 200:
            return True
        return False
