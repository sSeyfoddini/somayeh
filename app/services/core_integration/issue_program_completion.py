import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.program_completion_model import ProgramCompletionModel

_log = logging.getLogger(__name__)


class IssueProgramCompletion:
    @classmethod
    def issue_program_completion(cls, external_id: str, program_completion_schema: ProgramCompletionModel):
        _log.info(program_completion_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ProgramCompletion.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": program_completion_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        program_completion_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {program_completion_response.text}")
        if program_completion_response.status_code == 200:
            return True
        return False
