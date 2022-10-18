import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.class_withdrawal_model import ClassWithdrawalModel

_log = logging.getLogger(__name__)


class IssueClassWithdrawal:
    @classmethod
    def issue_class_withdrawal(cls, external_id: str, class_withdrawal_schema: ClassWithdrawalModel):
        _log.info(class_withdrawal_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ClassWithdrawal.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": class_withdrawal_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        class_withdrawal_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {class_withdrawal_response.text}")
        if class_withdrawal_response.status_code == 200:
            return True
        return False
