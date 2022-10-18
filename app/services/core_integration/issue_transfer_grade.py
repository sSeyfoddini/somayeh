import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.transfer_grade_model import TransferGradeModel

_log = logging.getLogger(__name__)


class IssueTransferGrade:
    @classmethod
    def issue_transfer_grade(cls, external_id: str, transfer_grade_schema: TransferGradeModel):
        _log.info(transfer_grade_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/TransferGrade.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": transfer_grade_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        transfer_grade_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {transfer_grade_response.text}")
        if transfer_grade_response.status_code == 200:
            return True
        return False
