import logging
import os

import requests

from app.model.credential_schema_tables_model.instructor_role_model import InstructorRoleModel
from app.persistence.credential_schema_tables_persistence.instructor_role_persistence import InstructorRolePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class InstructorRoleService:
    @classmethod
    def add(cls, user_id, user_name, name, description, type, external_id):

        instructor_role = InstructorRoleModel(name=name, description=description, type=type, external_id=external_id)
        instructor_role = InstructorRolePersistence.add(user_id, user_name, instructor_role)
        return instructor_role

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        instructor_role = InstructorRolePersistence.get(uuid)

        if instructor_role is None:
            raise RecordNotFound("'instructor role' with uuid '{}' not found.".format(uuid))

        instructor_role = InstructorRoleModel(
            uuid=uuid,
            name=args.get("name", instructor_role.name),
            description=args.get("description", instructor_role.description),
            type=args.get("type", instructor_role.type),
            external_id=args.get("external_id", instructor_role.external_id)
        )
        instructor_role = InstructorRolePersistence.update(user_id, user_name, instructor_role)

        return instructor_role

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        instructor_role = InstructorRolePersistence.get(uuid)
        if instructor_role is None:
            raise RecordNotFound("'instructor role' with uuid '{}' not found.".format(uuid))
        InstructorRolePersistence.delete(user_id, user_name, instructor_role)
        return instructor_role

    @classmethod
    def get(cls, uuid):
        instructor_role = InstructorRolePersistence.get(uuid)
        if instructor_role is None:
            raise RecordNotFound("'instructor role' with uuid '{}' not found.".format(uuid))
        return instructor_role

    @classmethod
    def get_all(cls):
        return InstructorRolePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return InstructorRolePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = InstructorRolePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "instructor_role", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
