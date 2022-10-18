import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.student_affiliation_model import StudentAffiliationModel

_log = logging.getLogger(__name__)


class IssueStudentAffiliation:
    @classmethod
    def issue_student_affiliation(cls, external_id: str, student_affiliation_schema: StudentAffiliationModel):
        _log.info(student_affiliation_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/StudentAffiliation.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": student_affiliation_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        student_affiliation_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {student_affiliation_response.text}")
        if student_affiliation_response.status_code == 200:
            return True
        return False
