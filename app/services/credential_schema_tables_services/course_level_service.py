import logging
import os

import requests

from app.model.credential_schema_tables_model.course_level_model import CourseLevelModel
from app.persistence.credential_schema_tables_persistence.course_level_persistence import CourseLevelPersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class CourseLevelService:
    @classmethod
    def add(cls, user_id, user_name, name, description, type, external_id):

        course_level = CourseLevelModel(name=name, description=description, type=type, external_id=external_id)
        course_level = CourseLevelPersistence.add(user_id, user_name, course_level)
        return course_level

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        course_level = CourseLevelPersistence.get(uuid)

        if course_level is None:
            raise RecordNotFound("'course level' with uuid '{}' not found.".format(uuid))

        course_level = CourseLevelModel(
            uuid=uuid,
            name=args.get("name", course_level.name),
            description=args.get("description", course_level.description),
            type=args.get("type", course_level.type),
            external_id=args.get("external_id", course_level.external_id),
        )
        course_level = CourseLevelPersistence.update(user_id, user_name, course_level)

        return course_level

    @classmethod
    def delete(cls, user_id, user_name, course_level):
        CourseLevelPersistence.delete(user_id, user_name, course_level)
        return course_level

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        course_level = CourseLevelPersistence.get(uuid)
        if course_level is None:
            raise RecordNotFound("'course level' with uuid '{}' not found.".format(uuid))
        CourseLevelPersistence.delete(user_id, user_name, course_level)
        return course_level

    @classmethod
    def get(cls, uuid):
        course_level = CourseLevelPersistence.get(uuid)
        if course_level is None:
            raise RecordNotFound("'course level' with uuid '{}' not found.".format(uuid))
        return course_level

    @classmethod
    def get_all(cls):
        return CourseLevelPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CourseLevelPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = CourseLevelPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "course_level", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
