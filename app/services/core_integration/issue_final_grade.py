import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.final_grade_model import FinalGradeModel

_log = logging.getLogger(__name__)


class IssueFinalGrade:
    @classmethod
    def issue_final_grade(cls, external_id: str, final_grade_schema: FinalGradeModel):
        _log.info(final_grade_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/FinalGrade.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": final_grade_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        final_grade_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {final_grade_response.text}")
        if final_grade_response.status_code == 200:
            return True
        return False
