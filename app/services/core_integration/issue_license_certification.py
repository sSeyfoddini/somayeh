import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.license_certification_model import LicenseCertificationModel

_log = logging.getLogger(__name__)


class IssueLicenseCertification:
    @classmethod
    def issue_license_certification(cls, external_id: str, license_certification_schema: LicenseCertificationModel):
        _log.info(license_certification_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/LicenseCertification.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": license_certification_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        license_certification_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {license_certification_response.text}")
        if license_certification_response.status_code == 200:
            return True
        return False
