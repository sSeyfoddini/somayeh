import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.program_affiliation_model import ProgramAffiliationModel

_log = logging.getLogger(__name__)


class IssueProgramAffiliation:
    @classmethod
    def issue_program_affiliation(cls, external_id: str, program_affiliation_schema: ProgramAffiliationModel):
        _log.info(program_affiliation_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ProgramAffiliation.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": program_affiliation_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        program_affiliation_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {program_affiliation_response.text}")
        if program_affiliation_response.status_code == 200:
            return True
        return False
