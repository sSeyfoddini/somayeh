
from app import db
from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.model.credential_schema_tables_model.term_model import TermModel
from app.persistence.credential_schema_tables_persistence.term_persistence import TermPersistence
from app.services.thin_client_service import TermService


class Term:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"
        page = 1

        responses = []

        while True:
            response = TermService.get(limit, page)
            if not response:
                break
            responses.append(response)
            page = page + 1

        db.session.query(TermModel).delete()

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid).filter(CredentialTypeModel.name == "term").scalar()
        )
        for response in responses:
            for data in response:
                term = TermModel(
                    name=data["name"] if "name" in data else "",
                    start_date=data["start_date"] if "start_date" in data else None,
                    end_date=data["end_date"] if "end_date" in data else None,
                    session_id=data["session_id"] if "session_id" in data else "",
                    type=data["type"] if "type" in data else "",
                    external_id=data["external_id"],
                    credential_type_id=credential_type_id,
                    parent_organization=parent_organization,
                )
                TermPersistence.add(user_id, user_name, term)