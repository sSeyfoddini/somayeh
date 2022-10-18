
from app import db

from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.model.credential_schema_tables_model.general_education_group_asu_model import GeneralEducationGroupASUModel
from app.persistence.credential_schema_tables_persistence.general_education_group_asu_persistence import (
    GeneralEducationGroupASUPersistence,
)
from app.services.thin_client_service import GeneralEducationGroupService


class GeneralEducationGroup:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"
        page = 1

        responses = []

        while True:
            response = GeneralEducationGroupService.get(page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        db.session.query(GeneralEducationGroupASUModel).delete()

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid)
            .filter(CredentialTypeModel.name == "general_education_group_asu")
            .scalar()
        )
        for response in responses:
            for data in response:
                general = GeneralEducationGroupASUModel(
                    name=data["name"] if "name" in data else "",
                    description=data["description"] if "description" in data else "",
                    external_id=data["external_id"] if "external_id" in data else "",
                    gen_id_list=data["gen_id_list"] if "gen_id_list" in data else None,
                    gen_code_list=data["gen_code_list"] if "gen_code_list" in data else "",
                    credential_type_id=credential_type_id,
                    parent_organization=parent_organization
                )
                GeneralEducationGroupASUPersistence.add(user_id, user_name, general)

