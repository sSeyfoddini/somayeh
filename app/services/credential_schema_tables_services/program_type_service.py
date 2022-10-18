import logging
import os

import requests

from app.model.credential_schema_tables_model.program_type_model import ProgramTypeModel
from app.persistence.credential_schema_tables_persistence.program_type_persistence import ProgramTypePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class ProgramTypeService:
    @classmethod
    def add(cls, user_id, user_name, name, description, type, external_id):

        program_type = ProgramTypeModel(name=name, description=description, type=type, external_id=external_id)
        program_type = ProgramTypePersistence.add(user_id, user_name, program_type)
        return program_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        program_type = ProgramTypePersistence.get(uuid)

        if program_type is None:
            raise RecordNotFound("'program type' with uuid '{}' not found.".format(uuid))

        program_type = ProgramTypeModel(
            uuid=uuid,
            name=args.get("name", program_type.name),
            description=args.get("description", program_type.description),
            type=args.get("type", program_type.type),
            external_id=args.get("external_id", program_type.external_id),
        )
        program_type = ProgramTypePersistence.update(user_id, user_name, program_type)

        return program_type

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        program_type = ProgramTypePersistence.get(uuid)
        if program_type is None:
            raise RecordNotFound("'program type' with uuid '{}' not found.".format(uuid))
        ProgramTypePersistence.delete(user_id, user_name, program_type)
        return program_type

    @classmethod
    def get(cls, uuid):
        program_type = ProgramTypePersistence.get(uuid)
        if program_type is None:
            raise RecordNotFound("'program type' with uuid '{}' not found.".format(uuid))
        return program_type

    @classmethod
    def get_all(cls):
        return ProgramTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ProgramTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = ProgramTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "program_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
