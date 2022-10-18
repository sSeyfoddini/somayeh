import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.transcript_model import TranscriptModel

_log = logging.getLogger(__name__)


class IssueTranscript:
    @classmethod
    def issue_transcript(cls, external_id: str, transcript_schema: TranscriptModel):
        _log.info(transcript_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Transcript.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": transcript_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        transcript_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {transcript_response.text}")
        if transcript_response.status_code == 200:
            return True
        return False
