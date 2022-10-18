import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.course_model import CourseModel

_log = logging.getLogger(__name__)


class IssueCourse:
    @classmethod
    def issue_course(cls, external_id: str, course_schema: CourseModel):
        _log.info(course_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/Course.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": course_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        course_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {course_response.text}")
        if course_response.status_code == 200:
            return True
        return False
