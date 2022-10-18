import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.user_identity_model import UserIdentitySchemaModel

_log = logging.getLogger(__name__)


class IssueUserIdentity:
    @classmethod
    def issue_identity(cls, user_identity_schema: UserIdentitySchemaModel, external_id: str):
        _log.info(f"Issuing User Identity with external_id: {external_id}")
        print(f"Issuing User Identity with external_id: {external_id}")
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/UserIdentity.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": user_identity_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        user_identity_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {user_identity_response.text}")
        print(f"Response from core {user_identity_response.text}")
        if user_identity_response.status_code == 200:
            return True
        return False
