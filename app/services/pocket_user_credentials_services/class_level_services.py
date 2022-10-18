import logging
import os

import requests

from app.model.pocket_user_credentials_model.class_level_model import ClassLevelModel
from app.persistence.pocket_user_credentials_persistence.class_level_persistence import ClassLevelPersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class ClassLevelService:
    @classmethod
    def add(cls, user_id, user_name, level, description, semester_order, type, external_id):

        class_level = ClassLevelModel(
            level=level,
            description=description,
            semester_order=semester_order,
            type=type,
            external_id=external_id,
        )
        class_level = ClassLevelPersistence.add(user_id, user_name, class_level)
        return class_level

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        class_level = ClassLevelPersistence.get(uuid)

        if class_level is None:
            raise RecordNotFound("'class level' with uuid '{}' not found.".format(uuid))

        class_level = ClassLevelModel(
            uuid=uuid,
            level=args.get("level", class_level.level),
            description=args.get("description", class_level.description),
            semester_order=args.get("semester_order", class_level.semester_order),
            type=args.get("type", class_level.type),
            external_id=args.get("external_id", class_level.external_id),
        )
        class_level = ClassLevelPersistence.update(user_id, user_name, class_level)

        return class_level

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        class_level = ClassLevelPersistence.get(uuid)
        if class_level is None:
            raise RecordNotFound("'class level' with uuid '{}' not found.".format(uuid))
        ClassLevelPersistence.delete(user_id, user_name, class_level)
        return class_level

    @classmethod
    def get(cls, uuid):
        class_level = ClassLevelPersistence.get(uuid)
        if class_level is None:
            raise RecordNotFound("'class level' with uuid '{}' not found.".format(uuid))
        return class_level

    @classmethod
    def get_all(cls):
        return ClassLevelPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ClassLevelPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = ClassLevelPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "class_level", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
