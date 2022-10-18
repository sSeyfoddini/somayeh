import logging
import os

import requests

from app.model.credential_schema_tables_model.coursework_type_model import CourseworkTypeModel
from app.persistence.credential_schema_tables_persistence.coursework_type_persistence import CourseworkTypePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class CourseworkTypeService:
    @classmethod
    def add(cls, user_id, user_name, name, description, type, external_id):

        coursework_type = CourseworkTypeModel(name=name, description=description, type=type, external_id=external_id)
        coursework_type = CourseworkTypePersistence.add(user_id, user_name, coursework_type)
        return coursework_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        coursework_type = CourseworkTypePersistence.get(uuid)

        if coursework_type is None:
            raise RecordNotFound("'coursework' with uuid '{}' not found.".format(uuid))

        coursework_type = CourseworkTypeModel(
            uuid=uuid,
            name=args.get("name", coursework_type.name),
            description=args.get("description", coursework_type.description),
            type=args.get("type", coursework_type.type),
            external_id=args.get("external_id", coursework_type.external_id),
        )
        coursework_type = CourseworkTypePersistence.update(user_id, user_name, coursework_type)

        return coursework_type

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        coursework_type = CourseworkTypePersistence.get(uuid)
        if coursework_type is None:
            raise RecordNotFound("'coursework' with uuid '{}' not found.".format(uuid))
        CourseworkTypePersistence.delete(user_id, user_name, coursework_type)
        return coursework_type

    @classmethod
    def get(cls, uuid):
        coursework_type = CourseworkTypePersistence.get(uuid)
        if coursework_type is None:
            raise RecordNotFound("'coursework' with uuid '{}' not found.".format(uuid))
        return coursework_type

    @classmethod
    def get_all(cls):
        return CourseworkTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CourseworkTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = CourseworkTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "coursework_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
