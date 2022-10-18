import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.general_education_ful_fillment_model import GeneralEducationFulFillmentModel

_log = logging.getLogger(__name__)


class IssueGeneralEducationFulFillment:
    @classmethod
    def issue_general_education_ful_fillment(
        cls, external_id: str, general_education_ful_fillment_schema: GeneralEducationFulFillmentModel
    ):
        _log.info(general_education_ful_fillment_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/GeneralEducationFulFillment.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": general_education_ful_fillment_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        general_education_ful_fillment_response = requests.post(
            Config.pocket_core_api_credential, headers=headers, json=PARAMS
        )
        _log.info(f"Response from core {general_education_ful_fillment_response.text}")
        if general_education_ful_fillment_response.status_code == 200:
            return True
        return False
