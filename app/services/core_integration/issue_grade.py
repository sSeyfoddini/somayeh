import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.grade_model import GradeModel

_log = logging.getLogger(__name__)


class IssueGrade:
    @classmethod
    def issue_grade(cls, external_id: str, grade_schema: GradeModel):
        _log.info(grade_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Grade.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": grade_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        grade_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {grade_response.text}")
        if grade_response.status_code == 200:
            return True
        return False
