import logging
import uuid

import requests

from app.config import Config
from app.model.core_integration.course_work_model import CourseWorkModel

_log = logging.getLogger(__name__)


class IssueCourseWork:
    @classmethod
    def issue_course_work(cls, external_id: str, course_work_schema: CourseWorkModel):
        _log.info(course_work_schema.to_dict())
        headers = {"content-type": "application/json"}
        PARAMS = {
            "external_connection_id": external_id,
            "schemas": ["https://schemas.getpocket.io/schema/CourseWork.json"],
            "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
            "comment": "",
            "attributes": course_work_schema.to_dict(),
            "metadata": {},
            "type": "UniversityCredential",
        }
        course_work_response = requests.post(Config.pocket_core_api_credential, headers=headers, json=PARAMS)
        _log.info(f"Response from core {course_work_response.text}")
        if course_work_response.status_code == 200:
            return True
        return False
