

from app import db
from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.model.role_model import RoleModel
from app.persistence.role_persistence import RolePersistence
from app.services.thin_client_service import RolesService



class Role:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"
        page = 1

        responses = []

        while True:
            response = RolesService.get(page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        db.session.query(RoleModel).delete()

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid).filter(CredentialTypeModel.name == "role").scalar()
        )
        for response in responses:
            for data in response:
                role = RoleModel(
                    name=data["name"] if "name" in data else "",
                    type=data["type"] if "type" in data else "",
                    external_id=data["external_id"] if "external_id" in data else "",
                    credential_type_id=credential_type_id,
                    parent_organization=parent_organization,
                )
                RolePersistence.add(user_id, user_name, role)

