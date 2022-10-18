import logging
import os

import requests

from app.model.credential_schema_tables_model.program_completion_model import ProgramCompletionModel
from app.persistence.credential_schema_tables_persistence.program_completion_persistence import (
    ProgramCompletionPersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class ProgramCompletionService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        credential_type_label,
        recognition_date,
        term_id,
        term_label,
        program_id,
        program_label,
        credential_label,
        type,
        external_id,
    ):

        program_completion = ProgramCompletionModel(
            credential_type_id=credential_type_id,
            credential_type_label=credential_type_label,
            recognition_date=recognition_date,
            term_id=term_id,
            term_label=term_label,
            program_id=program_id,
            program_label=program_label,
            credential_label=credential_label,
            type=type,
            external_id=external_id,
        )
        program_completion = ProgramCompletionPersistence.add(user_id, user_name, program_completion)
        return program_completion

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        program_completion = ProgramCompletionPersistence.get(uuid)

        if program_completion is None:
            raise RecordNotFound("'program completion' with uuid '{}' not found.".format(uuid))

        program_completion = ProgramCompletionModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", program_completion.credential_type_id),
            credential_type_label=args.get("credential_type_label", program_completion.credential_type_label),
            recognition_date=args.get("recognition_date", program_completion.recognition_date),
            term_id=args.get("term_id", program_completion.term_id),
            term_label=args.get("term_label", program_completion.term_label),
            program_id=args.get("program_id", program_completion.program_id),
            program_label=args.get("program_label", program_completion.program_label),
            credential_label=args.get("credential_label", program_completion.credential_label),
            type=args.get("type", program_completion.type),
            external_id=args.get("external_id", program_completion.external_id),
        )
        program_completion = ProgramCompletionPersistence.update(user_id, user_name, program_completion)

        return program_completion

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        program_completion = ProgramCompletionPersistence.get(uuid)
        if program_completion is None:
            raise RecordNotFound("'program completion' with uuid '{}' not found.".format(uuid))
        ProgramCompletionPersistence.delete(user_id, user_name, program_completion)
        return program_completion

    @classmethod
    def get(cls, id):
        program_completion = ProgramCompletionPersistence.get(id)
        if program_completion is None:
            raise RecordNotFound("'program completion' with uuid '{}' not found.".format(uuid))
        return program_completion

    @classmethod
    def get_all(cls):
        return ProgramCompletionPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ProgramCompletionPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = ProgramCompletionPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "program_completion", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
