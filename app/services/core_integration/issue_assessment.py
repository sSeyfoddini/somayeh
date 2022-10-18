import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.assessment_model import AssessmentModel

_log = logging.getLogger(__name__)


class IssueAssessment:
    @classmethod
    def issue_assessment(cls, external_id: str, assessment_schema: AssessmentModel):
        _log.info(assessment_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Assessment.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": assessment_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        assessment_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {assessment_response.text}")
        if assessment_response.status_code == 200:
            return True
        return False
