import copy
import logging
import os
import uuid
import requests

from app.model.credential_schema_tables_model.badge_type_model import BadgeTypeModel
from app.persistence.credential_schema_tables_persistence.badge_type_persistence import BadgeTypePersistence
from app.services.badgr_service import BadgrService
from app.services.image_service import ImageService
from app.services.issue_params import set_params
from app.config import Config
from app.services.pocket_user_credentials_services.organizations_services import OrganizationsService
from app.services.credential_schema_tables_services.badge_partner_service import BadgePartnerService
from app.util.error_handlers import InvalidImage, RecordNotFound


class BadgeTypeService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        extrernal_partner_id,
        extrernal_partner_label,
        badge_org_type,
        badge_org_id,
        badge_org_label,
        name,
        abbreviation,
        description,
        external_id,
        reference_uri,
        image,
        attachment,
        type,
        json,
        credential_type_uuid,
        org_uuid,
        entityID,
        auto_issue
    ):

        badge_type = BadgeTypeModel(
            extrernal_partner_id=extrernal_partner_id,
            extrernal_partner_label=extrernal_partner_label,
            badge_org_type=badge_org_type,
            badge_org_id=badge_org_id,
            badge_org_label=badge_org_label,
            name=name,
            abbreviation=abbreviation,
            description=description,
            external_id=external_id,
            reference_uri=reference_uri,
            image=image,
            attachment=attachment,
            type=type,
            json=json,
            credential_type_uuid=credential_type_uuid,
            org_uuid=org_uuid,
            entityID=entityID,
            auto_issue=auto_issue
        )
        badge_type = BadgeTypePersistence.add(user_id, user_name, badge_type)
        return badge_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        badge_type = BadgeTypePersistence.get(uuid)

        if badge_type is None:
            raise RecordNotFound("'badge_type' with uuid '{}' not found.".format(uuid))

        if "image" in args:
            image = args["image"].read()
            if image:
                valid_image, image_data = ImageService.image_validation(image)
                if valid_image:
                    image_name = ImageService.upload_file(image)
                    image_data.update({"image_name": image_name})
                    if badge_type.image:
                        ImageService.delete_image(badge_type.image["image_name"])
                else:
                    raise InvalidImage("'image' is invalid image.")
            else:
                image_data = None
        else:
            image_data = badge_type.image

        badge_type = BadgeTypeModel(
            uuid=uuid,
            extrernal_partner_id=args.get("extrernal_partner_id", badge_type.extrernal_partner_id),
            extrernal_partner_label=args.get("extrernal_partner_label", badge_type.extrernal_partner_label),
            badge_org_type=args.get("badge_org_type", badge_type.badge_org_type),
            badge_org_id=args.get("badge_org_id", badge_type.badge_org_id),
            badge_org_label=args.get("badge_org_label", badge_type.badge_org_label),
            name=args.get("name", badge_type.name),
            abbreviation=args.get("abbreviation", badge_type.abbreviation),
            description=args.get("description", badge_type.description),
            external_id=args.get("external_id", badge_type.external_id),
            reference_uri=args.get("reference_uri", badge_type.reference_uri),
            image=image_data,
            attachment=args.get("attachment", badge_type.attachment),
            type=args.get("type", badge_type.type),
            json=args.get("json", badge_type.json),
            credential_type_uuid=args.get("credential_type_uuid", badge_type.credential_type_uuid),
            org_uuid=args.get("org_uuid", badge_type.org_uuid),
            entityID=args.get("entityID", badge_type.entityID),
            auto_issue=args.get("auto_issue", badge_type.auto_issue)
        )
        badge_type = BadgeTypePersistence.update(user_id, user_name, badge_type)

        return badge_type

    @classmethod
    def delete_all(cls, user_id, user_name):
        all_data=BadgeTypePersistence.get_all()
        for item in all_data:
            cls.delete_by_uuid(user_id, user_name, item.uuid)

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        badge_type = BadgeTypePersistence.get(uuid)
        if badge_type is None:
            raise RecordNotFound("'badge_type' with uuid '{}' not found.".format(uuid))
        BadgeTypePersistence.delete(user_id, user_name, badge_type)
        if badge_type.image:
            ImageService.delete_image(badge_type.image["image_name"])
        return badge_type

    @classmethod
    def get(cls, uuid):
        badge_type = BadgeTypePersistence.get(uuid)
        if badge_type is None:
            raise RecordNotFound("'badge_type' with uuid '{}' not found.".format(uuid))

        if badge_type.image:
            badge_type = copy.deepcopy(badge_type)
            badge_type.image = ImageService.get_image(badge_type.image["image_name"])
        return badge_type

    @classmethod
    def get_by_entityID(cls, entityID):
        return BadgeTypePersistence.get_by_entityID(entityID)

    @classmethod
    def get_all_by_filter(cls, filter_dict):

        badge_types, total_records, page = BadgeTypePersistence.get_all_by_filter(filter_dict)
        badge_types = copy.deepcopy(badge_types)
        if badge_types:
            for badge_type in badge_types:
                if badge_type.image:
                    badge_type.image = ImageService.get_image(badge_type.image["image_name"])
        return badge_types, total_records, page

    @classmethod
    def issue_badge(cls, external_id: str):
        badges = BadgeTypeModel.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"
        print(badges)
        for badge in badges:
            PARAMS = {
                "external_connection_id": external_id,
                "external_schema_id": "badge",
                "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
                "comment": "",
                "attributes": badge.serialized,
            }
            requests.post(pocket_core_api_credential, json=PARAMS)

    @classmethod
    def issue(cls, external_id: str):
        records = BadgeTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "badge_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)

    @classmethod
    def update_from_badgr_single(cls, user_id, user_name, uuid):
        old_badge_type = cls.get(uuid)
        if old_badge_type.entityID:
            access_token, refresh_token = BadgrService.authanticate(Config.BADGER_USERNAME, Config.BADGER_PASSWORD)
            hed = {"Authorization": "Bearer " + access_token}
            uri = "https://api.badgr.io/v2/badgeclasses/"+ old_badge_type.entityID
            response = requests.get(uri, headers=hed).json()
            data = response['result'][0]

            new_badge_type = BadgeTypeModel(
                uuid=uuid,
                extrernal_partner_id=old_badge_type.extrernal_partner_id,
                extrernal_partner_label=old_badge_type.extrernal_partner_label,
                badge_org_type=old_badge_type.badge_org_type,
                badge_org_id=old_badge_type.badge_org_id,
                badge_org_label=old_badge_type.badge_org_label,
                name=data["name"],
                abbreviation=old_badge_type.abbreviation,
                description=data["description"],
                external_id=old_badge_type.external_id,
                reference_uri=old_badge_type.reference_uri,
                image=old_badge_type.image,
                attachment=old_badge_type.attachment,
                type=old_badge_type.type,
                json=old_badge_type.json,
                credential_type_uuid=old_badge_type.credential_type_uuid,
                org_uuid=old_badge_type.org_uuid,
                entityID=old_badge_type.entityID,
                auto_issue=old_badge_type.auto_issue
                )
            BadgeTypePersistence.update(user_id, user_name, new_badge_type)

    @classmethod
    def update_from_badgr_by_org_uuid(cls, user_id, username, uuid):
        organization = OrganizationsService.get(uuid)
        if organization and organization.issuer_id:

            access_token, refresh_token = BadgrService.authanticate(Config.BADGER_USERNAME, Config.BADGER_PASSWORD)
            response = BadgrService.badge_type_get_all_badges(access_token, [organization.issuer_id])

            for data in response:
                old_badge_type = BadgeTypeService.get_by_entityID(data["entityId"])
                if old_badge_type:
                    #update
                    new_badge_type = BadgeTypeModel(
                        uuid=uuid,
                        extrernal_partner_id=old_badge_type.extrernal_partner_id,
                        extrernal_partner_label=old_badge_type.extrernal_partner_label,
                        badge_org_type=old_badge_type.badge_org_type,
                        badge_org_id=old_badge_type.badge_org_id,
                        badge_org_label=old_badge_type.badge_org_label,
                        name=data["name"],
                        abbreviation=old_badge_type.abbreviation,
                        description=data["description"],
                        external_id=old_badge_type.external_id,
                        reference_uri=old_badge_type.reference_uri,
                        image=old_badge_type.image,
                        attachment=old_badge_type.attachment,
                        type=old_badge_type.type,
                        json=old_badge_type.json,
                        credential_type_uuid=old_badge_type.credential_type_uuid,
                        org_uuid=uuid,
                        entityID=old_badge_type.entityID,
                        auto_issue=old_badge_type.auto_issue
                    )
                    BadgeTypePersistence.update(user_id, username, new_badge_type)
                else:
                    #insert
                    BadgeTypeService.add(
                        user_id=user_id,
                        user_name=username,
                        extrernal_partner_id="",
                        extrernal_partner_label="",
                        badge_org_type="",
                        badge_org_id=None,
                        badge_org_label="",
                        name=data["name"],
                        abbreviation="",
                        description=data["description"],
                        external_id="",
                        reference_uri="",
                        image=None,
                        attachment=None,
                        type="",
                        json="",
                        credential_type_uuid="",
                        org_uuid=uuid,
                        entityID=data["entityId"],
                        auto_issue=False
                    )
    @classmethod
    def insert_all_from_badgr(cls, user_id, username):
        access_token, refresh_token = BadgrService.authanticate(Config.BADGER_USERNAME, Config.BADGER_PASSWORD)
        entityId = BadgrService.get_issusers_entityid(access_token)
        result = BadgrService.badge_type_get_all_badges(access_token, entityId)

        badge_partner = BadgePartnerService.get_by_url("https://badgr.com/")
        for badges in result:
            for data in badges:
                organization = OrganizationsService.get_by_badgr_entityId(data["entityId"])
                old_badge_type = BadgeTypeService.get_by_entityID(data["entityId"])
                image_data = cls.get_image(data["image"])
                if old_badge_type:
                    # update
                    new_badge_type = BadgeTypeModel(
                        uuid=old_badge_type.uuid,
                        extrernal_partner_id=badge_partner.uuid,
                        extrernal_partner_label=badge_partner.name,
                        badge_org_type=organization.type_name if organization else "",
                        badge_org_id=organization.uuid if organization else "",
                        badge_org_label=organization.name if organization else "",
                        name=data["name"],
                        abbreviation="n/a",
                        description=data["description"],
                        external_id="",
                        reference_uri=data["openBadgeId"],
                        image=image_data,
                        attachment=old_badge_type.attachment,
                        type="education",
                        json=str(data),
                        credential_type_uuid="",
                        org_uuid=organization.uuid if organization else "",
                        entityID=data["entityId"],
                        auto_issue=old_badge_type.auto_issue
                    )
                    BadgeTypePersistence.update(user_id, username, new_badge_type)
                else:
                    # insert
                    BadgeTypeService.add(
                        user_id=user_id,
                        user_name=username,
                        extrernal_partner_id=badge_partner.uuid,
                        extrernal_partner_label=badge_partner.name,
                        badge_org_type=organization.type_name if organization else "",
                        badge_org_id=organization.uuid if organization else "",
                        badge_org_label=organization.name if organization else "",
                        name=data["name"],
                        abbreviation="n/a",
                        description=data["description"],
                        external_id="",
                        reference_uri=data["openBadgeId"],
                        image=image_data,
                        attachment=None,
                        type="education",
                        json=str(data),
                        credential_type_uuid="",
                        org_uuid=organization.uuid if organization else "",
                        entityID=data["entityId"],
                        auto_issue=False
                    )

    @classmethod
    def get_all_uuid(cls):
        return BadgeTypePersistence.get_all_uuid()

    @classmethod
    def get_image(cls,url):
        image_url = requests.head(url, allow_redirects=True).url
        image = requests.get(image_url).content
        valid, image_data = ImageService.image_validation(image)
        image_name = ImageService.upload_file(image)
        image_data.update({"image_name": image_name})

        return image_data
