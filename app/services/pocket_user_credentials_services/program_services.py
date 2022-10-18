import logging
import os

import requests

from app.model.pocket_user_credentials_model.program_model import ProgramModel
from app.persistence.pocket_user_credentials_persistence.program_persistence import ProgramPersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class ProgramService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        program_id,
        program_label,
        external_id,
        program_type_label,
        date,
        type,
        parent_organization,
    ):

        program = ProgramModel(
            credential_type_id=credential_type_id,
            program_id=program_id,
            program_label=program_label,
            external_id=external_id,
            program_type_label=program_type_label,
            date=date,
            type=type,
            parent_organization=parent_organization
        )
        program = ProgramPersistence.add(user_id, user_name, program)
        return program

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        program = ProgramPersistence.get(uuid)

        if program is None:
            raise RecordNotFound("'program' with uuid '{}' not found.".format(uuid))

        program = ProgramModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", program.credential_type_id),
            program_id=args.get("program_id", program.program_id),
            program_label=args.get("program_label", program.program_label),
            external_id=args.get("external_id", program.external_id),
            program_type_label=args.get("program_type_label", program.program_type_label),
            date=args.get("date", program.date),
            type=args.get("type", program.type),
            parent_organization=args.get("parent_organization", program.parent_organization),
        )
        program = ProgramPersistence.update(user_id, user_name, program)

        return program

    @classmethod
    def delete_all(cls):
        ProgramPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        program = ProgramPersistence.get(uuid)
        if program is None:
            raise RecordNotFound("'program' with uuid '{}' not found.".format(uuid))
        ProgramPersistence.delete(user_id, user_name, program)
        return program

    @classmethod
    def get(cls, uuid):
        program = ProgramPersistence.get(uuid)
        if program is None:
            raise RecordNotFound("'program' with uuid '{}' not found.".format(uuid))
        return program

    @classmethod
    def get_all(cls):
        return ProgramPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ProgramPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = ProgramPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "program", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
