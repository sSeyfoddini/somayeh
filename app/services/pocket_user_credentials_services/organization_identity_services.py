import logging
import os

import requests

from app.model.pocket_user_credentials_model.organization_identity_model import OrganizationIdentityModel
from app.persistence.pocket_user_credentials_persistence.organization_identity_persistence import (
    OrganizationIdentityPersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class OrganizationIdentityService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        organization_label,
        abbreviation,
        organization_type_id,
        organization_type_label,
        organization_subtype_id,
        organization_subtype_label,
        organization_parent_id,
        organization_parent_label,
        logo,
        background,
        reference_url,
        street_1,
        street_2,
        country,
        city,
        region,
        postal_code,
        type,
        external_id,
        parent_organization,
    ):

        organization_identity = OrganizationIdentityModel(
            credential_type_id=credential_type_id,
            organization_label=organization_label,
            abbreviation=abbreviation,
            organization_type_id=organization_type_id,
            organization_type_label=organization_type_label,
            organization_subtype_id=organization_subtype_id,
            organization_subtype_label=organization_subtype_label,
            organization_parent_id=organization_parent_id,
            organization_parent_label=organization_parent_label,
            logo=logo,
            background=background,
            reference_url=reference_url,
            street_1=street_1,
            street_2=street_2,
            country=country,
            city=city,
            region=region,
            postal_code=postal_code,
            type=type,
            external_id=external_id,
            parent_organization=parent_organization,
        )
        organization_identity = OrganizationIdentityPersistence.add(user_id, user_name, organization_identity)
        return organization_identity

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        organization_identity = OrganizationIdentityPersistence.get(uuid)

        if organization_identity is None:
            raise RecordNotFound("'organization identity' with uuid '{}' not found.".format(uuid))

        organization_identity = OrganizationIdentityModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", organization_identity.credential_type_id),
            organization_label=args.get("organization_label", organization_identity.organization_label),
            abbreviation=args.get("abbreviation", organization_identity.abbreviation),
            organization_type_id=args.get("organization_type_id", organization_identity.organization_type_id),
            organization_type_label=args.get("organization_type_label", organization_identity.organization_type_label),
            organization_subtype_id=args.get("organization_subtype_id", organization_identity.organization_subtype_id),
            organization_subtype_label=args.get("organization_subtype_label",
                                                organization_identity.organization_subtype_label),
            organization_parent_id=args.get("organization_parent_id", organization_identity.organization_parent_id),
            organization_parent_label=args.get("organization_parent_label",
                                               organization_identity.organization_parent_label),
            logo=args.get("logo", organization_identity.logo),
            background=args.get("background", organization_identity.background),
            reference_url=args.get("reference_url", organization_identity.reference_url),
            street_1=args.get("street_1", organization_identity.street_1),
            street_2=args.get("street_2", organization_identity.street_2),
            country=args.get("country", organization_identity.country),
            city=args.get("city", organization_identity.city),
            region=args.get("region", organization_identity.region),
            postal_code=args.get("postal_code", organization_identity.postal_code),
            type=args.get("type", organization_identity.type),
            external_id=args.get("external_id", organization_identity.external_id),
            parent_organization=args.get("parent_organization", organization_identity.parent_organization)
        )
        organization_identity = OrganizationIdentityPersistence.update(user_id, user_name, organization_identity)

        return organization_identity

    @classmethod
    def delete_all(cls):
        OrganizationIdentityPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        organization_identity = OrganizationIdentityPersistence.get(uuid)
        if organization_identity is None:
            raise RecordNotFound("'organization identity' with uuid '{}' not found.".format(uuid))
        OrganizationIdentityPersistence.delete(user_id, user_name, organization_identity)
        return organization_identity

    @classmethod
    def get(cls, uuid):
        organization_identity = OrganizationIdentityPersistence.get(uuid)
        if organization_identity is None:
            raise RecordNotFound("'organization identity' with uuid '{}' not found.".format(uuid))
        return organization_identity

    @classmethod
    def get_all(cls):
        return OrganizationIdentityPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return OrganizationIdentityPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = OrganizationIdentityPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "organization_identity", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
