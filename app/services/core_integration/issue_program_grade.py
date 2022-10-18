import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.program_grade_model import ProgramGradeModel

_log = logging.getLogger(__name__)


class IssueProgramGrade:
    @classmethod
    def issue_program_grade(cls, external_id: str, program_grade_schema: ProgramGradeModel):
        _log.info(program_grade_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ProgramGrade.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": program_grade_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        program_grade_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {program_grade_response.text}")
        if program_grade_response.status_code == 200:
            return True
        return False
