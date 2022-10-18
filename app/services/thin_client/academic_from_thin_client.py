
from app.services.credential_schema_tables_services.credential_type_service import CredentialTypeService
from app.persistence.pocket_user_credentials_persistence.organizations_persistence import OrganizationsModel, \
    OrganizationsPersistence
from app.services.thin_client_service import AcademicInfoService

class Academic:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        type_name = "educational"
        input = {"term_code": "2221"}
        page = 1

        responses = []

        while True:
            response = AcademicInfoService.get(input, page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        OrganizationsPersistence.delete_all()

        credential_type, x, y = CredentialTypeService.get_all_by_filter({"name": type_name})

        if not credential_type:
            raise Exception("Insert credential type table.")

        type_id = credential_type[0].uuid

        for response in responses:
            for data in response:
                organization = OrganizationsModel(
                    name=data["name"],
                    description="",
                    abbreviation=data["abbreviation"],
                    type_id=type_id,
                    type_name=data["type_name"],
                    subtype_id=None,
                    parent_id=None,
                    parent_name="",
                    reference_url="",
                    logo="",
                    background="",
                    mail="",
                    street_1="",
                    street_2="",
                    country="",
                    city="",
                    region="",
                    postal_code="",
                    external_id=data["external_id"],
                    external_name="",
                    badgr_entityID="",
                    issuer_id="",
                )
                OrganizationsPersistence.add(user_id, user_name, organization)