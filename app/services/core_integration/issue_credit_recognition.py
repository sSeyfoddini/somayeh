import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.credit_recognition_model import CreditRecognitionModel

_log = logging.getLogger(__name__)


class IssueCreditRecognition:
    @classmethod
    def issue_credit_recognition(cls, external_id: str, credit_recognition_schema: CreditRecognitionModel):
        _log.info(credit_recognition_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/CreditRecognition.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": credit_recognition_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        credit_recognition_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {credit_recognition_response.text}")
        if credit_recognition_response.status_code == 200:
            return True
        return False
