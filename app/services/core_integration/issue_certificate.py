import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.certificate_model import CertificateModel

_log = logging.getLogger(__name__)


class IssueCertificate:
    @classmethod
    def issue_certificate(cls, external_id: str, certificate_schema: CertificateModel):
        _log.info(certificate_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Certificate.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": certificate_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        certificate_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {certificate_response.text}")
        if certificate_response.status_code == 200:
            return True
        return False
