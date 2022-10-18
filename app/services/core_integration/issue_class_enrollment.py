import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.class_enrollment_model import ClassEnrollmentModel

_log = logging.getLogger(__name__)


class IssueClassEnrollment:
    @classmethod
    def issue_class_enrollment(cls, external_id: str, class_enrollment_schema: ClassEnrollmentModel):
        _log.info(class_enrollment_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/ClassEnrollment.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": class_enrollment_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        class_enrollment_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {class_enrollment_response.text}")
        if class_enrollment_response.status_code == 200:
            return True
        return False
