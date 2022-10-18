
from app import db
from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.model.pocket_user_credentials_model.organization_identity_model import OrganizationIdentityModel
from app.persistence.pocket_user_credentials_persistence.organization_identity_persistence import (
    OrganizationIdentityPersistence,
)
from app.services.thin_client_service import OrgLocationService


class OrgIdentity:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"

        input = {"data": [{"ext_org_id": "1100100071", "org_location": "1"}], "max_date": 1}
        page = 1

        responses = []

        while True:
            response = OrgLocationService.get(input, page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid)
            .filter(CredentialTypeModel.name == "organization_identity")
            .scalar()
        )

        for response in responses:
            for datas in response:
                for data in datas:
                    old_org_identity = OrganizationIdentityPersistence.get_by_external_user_id(data["external_id"])
                    if old_org_identity:
                        # update table
                        old_org_identity = old_org_identity[0]
                        org_identity = OrganizationIdentityModel(
                            uuid=old_org_identity.uuid,
                            credential_type_id=credential_type_id,
                            organization_label=data.get("organization_label", old_org_identity.organization_label),
                            abbreviation=data.get("abbreviation", old_org_identity.abbreviation),
                            organization_type_id=data.get("organization_type_id", old_org_identity.organization_type_id),
                            organization_type_label=data.get("organization_type_label", old_org_identity.organization_type_label),
                            organization_subtype_id=data.get("organization_subtype_id", old_org_identity.organization_subtype_id),
                            organization_subtype_label=data.get("organization_subtype_id", old_org_identity.organization_subtype_label),
                            organization_parent_id=data.get("organization_parent_id", old_org_identity.organization_parent_id),
                            organization_parent_label=data.get("organization_parent_id", old_org_identity.organization_parent_label),
                            logo=data.get("logo", old_org_identity.logo),
                            background=data.get("background", old_org_identity.background),
                            reference_url=data.get("reference_url", old_org_identity.reference_url),
                            street_1=data.get("street_1", old_org_identity.street_1),
                            street_2=data.get("street_2", old_org_identity.street_2),
                            country=data.get("country", old_org_identity.country),
                            city=data.get("city", old_org_identity.city),
                            region=data.get("region", old_org_identity.region),
                            postal_code=data.get("postal_code", old_org_identity.postal_code),
                            type=data.get("type", old_org_identity.type),
                            external_id=data["external_id"],
                            parent_organization=parent_organization,
                        )
                        OrganizationIdentityPersistence.update(user_id, user_name, org_identity)
                    else:
                        # insert in table
                        org_identity = OrganizationIdentityModel(
                            credential_type_id=credential_type_id,
                            organization_label=data.get("organization_label"),
                            abbreviation=data.get("abbreviation"),
                            organization_type_id=data.get("organization_type_id"),
                            organization_type_label=data.get("organization_type_label"),
                            organization_subtype_id=data.get("organization_subtype_id"),
                            organization_subtype_label=data.get("organization_subtype_id"),
                            organization_parent_id=data.get("organization_parent_id"),
                            organization_parent_label=data.get("organization_parent_id"),
                            logo=data.get("logo"),
                            background=data.get("background"),
                            reference_url=data.get("reference_url"),
                            street_1=data.get("street_1"),
                            street_2=data.get("street_2"),
                            country=data.get("country"),
                            city=data.get("city"),
                            region=data.get("region"),
                            postal_code=data.get("postal_code"),
                            type=data.get("type"),
                            external_id=data["external_id"],
                            parent_organization=parent_organization,
                        )
                        OrganizationIdentityPersistence.add(user_id, user_name, org_identity)
