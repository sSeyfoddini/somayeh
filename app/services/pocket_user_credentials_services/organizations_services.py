import logging
import os

import requests

from app.model.pocket_user_credentials_model.organizations_model import OrganizationsModel
from app.persistence.pocket_user_credentials_persistence.organizations_persistence import OrganizationsPersistence
from app.services.issue_params import set_params
from app.services.image_service import ImageService
from app.util.error_handlers import InvalidImage, RecordNotFound


class OrganizationsService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        description,
        abbreviation,
        type_id,
        type_name,
        subtype_id,
        parent_id,
        parent_name,
        logo,
        background,
        reference_url,
        mail,
        street_1,
        street_2,
        country,
        city,
        region,
        postal_code,
        external_id,
        external_name,
        badgr_entityID,
        issuer_id
    ):

        organizations = OrganizationsModel(
            name=name,
            description=description,
            abbreviation=abbreviation,
            type_id=type_id,
            type_name=type_name,
            subtype_id=subtype_id,
            parent_id=parent_id,
            parent_name=parent_name,
            logo=logo,
            background=background,
            reference_url=reference_url,
            mail=mail,
            street_1=street_1,
            street_2=street_2,
            country=country,
            city=city,
            region=region,
            postal_code=postal_code,
            external_id=external_id,
            external_name=external_name,
            badgr_entityID=badgr_entityID,
            issuer_id=issuer_id
        )
        organizations = OrganizationsPersistence.add(user_id, user_name, organizations)
        return organizations

    @classmethod
    def update(cls, user_id, user_name, uuid, request):
        organizations = OrganizationsPersistence.get(uuid)

        if organizations is None:
            raise RecordNotFound("'organizations' with uuid '{}' not found.".format(uuid))

        if "logo" in request:
            logo_image = request["logo"].read()
            if logo_image:
                valid_logo_image, logo_image_data = ImageService.image_validation(logo_image)
                if valid_logo_image is False:
                    raise InvalidImage("'logo' is invalid image.")
            else:
                logo_image_data = None
        else:
            logo_image_data = organizations.logo

        if "background" in request:
            background_image = request["background"].read()
            if background_image:
                valid_background_image, background_image_data = ImageService.image_validation(background_image)
                if valid_background_image is False:
                    raise InvalidImage("'background' is invalid image.")
            else:
                background_image_data = None
        else:
            background_image_data = organizations.background

        if "logo" in request and logo_image_data:
            image_name = ImageService.upload_file(logo_image)
            logo_image_data.update({"image_name": image_name})
            if organizations.logo:
                ImageService.delete_image(organizations.logo["image_name"])

        if "background" in request and background_image_data:
            image_name = ImageService.upload_file(background_image)
            background_image_data.update({"image_name": image_name})
            if organizations.background:
                ImageService.delete_image(organizations.background["image_name"])

        organizations = OrganizationsModel(
            uuid=uuid,
            name=request.get("name", organizations.name),
            description=request.get("description", organizations.description),
            abbreviation=request.get("abbreviation", organizations.abbreviation),
            type_id=request.get("type_id", organizations.type_id),
            type_name=request.get("type_name", organizations.type_name),
            subtype_id=request.get("subtype_id", organizations.subtype_id),
            parent_id=request.get("parent_id", organizations.parent_id),
            parent_name=request.get("parent_name", organizations.parent_name),
            reference_url=request.get("reference_url", organizations.reference_url),
            logo=logo_image_data,
            background=background_image_data,
            mail=request.get("mail", organizations.mail),
            street_1=request.get("street_1", organizations.street_1),
            street_2=request.get("street_2", organizations.street_2),
            country=request.get("country", organizations.country),
            city=request.get("city", organizations.city),
            region=request.get("region", organizations.region),
            postal_code=request.get("postal_code", organizations.postal_code),
            external_id=request.get("external_id", organizations.external_id),
            external_name=request.get("external_name", organizations.external_name),
            badgr_entityID=request.get("badgr_entityID", organizations.badgr_entityID),
            issuer_id=request.get("issuer_id", organizations.issuer_id)
        )
        organizations = OrganizationsPersistence.update(user_id, user_name, organizations)

        return organizations

    @classmethod
    def delete_all(cls, user_id, user_name):
        all_data = OrganizationsPersistence.get_all()
        for item in all_data:
            cls.delete_by_uuid(user_id, user_name, item.uuid)


    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        organizations = OrganizationsPersistence.get(uuid)
        if organizations is None:
            raise RecordNotFound("'organizations' with uuid '{}' not found.".format(uuid))

        OrganizationsPersistence.delete(user_id, user_name, organizations)

        if organizations.logo:
            ImageService.delete_image(organizations.logo["image_name"])

        if organizations.background:
            ImageService.delete_image(organizations.background["image_name"])

        return organizations

    @classmethod
    def get(cls, uuid):
        organizations = OrganizationsPersistence.get(uuid)
        if organizations is None:
            raise RecordNotFound("'organizations' with uuid '{}' not found.".format(uuid))

        if organizations.logo:
            organizations.logo = ImageService.get_image(organizations.logo["image_name"])
        if organizations.background:
            organizations.background = ImageService.get_image(organizations.background["image_name"])
        return organizations

    @classmethod
    def get_all(cls):
        return OrganizationsPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        organizations, total_records, page = OrganizationsPersistence.get_all_by_filter(filter_dict)

        if organizations:
            for organization in organizations:
                if organization.logo:
                    organization.logo = ImageService.get_image(organization.logo["image_name"])
                if organization.background:
                    organization.background = ImageService.get_image(organization.background["image_name"])

        return organizations, total_records, page
    @classmethod
    def issue(cls, external_id: str):
        records = OrganizationsPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "organizations", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)

    @classmethod
    def get_by_badgr_entityId(cls, badgr_entityId):
        organizations = OrganizationsPersistence.get_by_badgr_entityId(badgr_entityId)
        return organizations