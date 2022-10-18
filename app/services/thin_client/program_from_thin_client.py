import logging
from uuid import uuid4

from app import db
from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.model.pocket_user_credentials_model.program_model import ProgramModel
from app.persistence.pocket_user_credentials_persistence.program_persistence import ProgramPersistence
from app.services.thin_client_service import ProgramsService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)


class Program:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"

        input = {"term_code": "2221"}
        page = 1

        responses = []

        while True:
            response = ProgramsService.get(input, page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        db.session.query(ProgramModel).delete()

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid).filter(CredentialTypeModel.name == "program").scalar()
        )
        for response in responses:
            for data in response:
                program = ProgramModel(
                    credential_type_id=credential_type_id,
                    program_id=data["program_id"] if "program_id" in data else "",
                    program_label=data["program_label"] if "program_label" in data else "",
                    external_id=data["external_id"] if "external_id" in data else "",
                    program_type_label=data["program_type_label"] if "program_type_label" in data else "",
                    date=data["date"] if "date" in data else None,
                    type=data["type"] if "type" in data else "",
                    parent_organization=parent_organization,
                    uuid=str(uuid4()),
                )
                ProgramPersistence.add(user_id, user_name, program)

