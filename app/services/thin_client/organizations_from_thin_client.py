

from app import db
from app.model.pocket_user_credentials_model.organizations_model import OrganizationsModel
from app.persistence.pocket_user_credentials_persistence.organizations_persistence import OrganizationsPersistence
from app.services.thin_client_service import CollegesService


class organizations:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"
        input = {"term_code": "2221"}
        page = 1

        responses = []

        while True:
            response = CollegesService.get(input, page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        db.session.query(OrganizationsModel).delete()

        for response in responses:
            for data in response:
                organizations = OrganizationsModel(name=data["name"])
                OrganizationsPersistence.add(user_id, user_name, organizations)

