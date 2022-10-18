import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.term_model import TermModel

_log = logging.getLogger(__name__)


class IssueTerm:
    @classmethod
    def issue_term(cls, external_id: str, term_schema: TermModel):
        _log.info(term_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Term.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": term_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        term_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {term_response.text}")
        if term_response.status_code == 200:
            return True
        return False
