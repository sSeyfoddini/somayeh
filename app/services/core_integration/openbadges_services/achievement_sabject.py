import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.openbadges_model.achievement_subject_model import AchievementSubjectModel

_log = logging.getLogger(__name__)


class IssueOpenBadgesAchievementSubject:
    @classmethod
    def issue_openbadges_achievement_subject(
        cls, external_id: str, openbadges_achievement_subject_schema: AchievementSubjectModel
    ):

        _log.info(openbadges_achievement_subject_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/openbadges/AchievementSubject.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": openbadges_achievement_subject_schema.to_dict(),
            "metadata": {},
            "type": "OpenBadgesAchievementSubjectCredential",
        }
        openbadges_achievement_subject_response = requests.post(
            Config.pocket_core_api_credential, headers=headers, json=PARAMS
        )
        _log.info(f"Response from core {openbadges_achievement_subject_response.text}")
        if openbadges_achievement_subject_response.status_code == 200:
            return True
        return False
