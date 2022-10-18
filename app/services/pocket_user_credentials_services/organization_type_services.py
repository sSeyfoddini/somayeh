import logging
import os

import pandas as pd
import requests

from app.model.pocket_user_credentials_model.organization_type_model import OrganizationTypeModel
from app.persistence.pocket_user_credentials_persistence.organization_type_persistence import (
    OrganizationTypePersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class OrganizationTypeService:
    @classmethod
    def add(cls, user_id, user_name, name, description, subtype_id):

        organization_type = OrganizationTypeModel(name=name, description=description, subtype_id=subtype_id)
        organization_type = OrganizationTypePersistence.add(user_id, user_name, organization_type)
        return organization_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        organization_type = OrganizationTypePersistence.get(uuid)

        if organization_type is None:
            raise RecordNotFound("'organization type' with uuid '{}' not found.".format(uuid))

        organization_type = OrganizationTypeModel(
            uuid=uuid,
            name=args.get("name", organization_type.name),
            description=args.get("description", organization_type.description),
            subtype_id=args.get("subtype_id", organization_type.subtype_id),
        )
        organization_type = OrganizationTypePersistence.update(user_id, user_name, organization_type)

        return organization_type

    @classmethod
    def delete_all(cls):
        OrganizationTypePersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        organization_type = OrganizationTypePersistence.get(uuid)
        if organization_type is None:
            raise RecordNotFound("'organization type' with uuid '{}' not found.".format(uuid))
        OrganizationTypePersistence.delete(user_id, user_name, organization_type)
        return organization_type

    @classmethod
    def get(cls, uuid):
        organization_type = OrganizationTypePersistence.get(uuid)
        if organization_type is None:
            raise RecordNotFound("'organization type' with uuid '{}' not found.".format(uuid))
        return organization_type

    @classmethod
    def get_all(cls):
        return OrganizationTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return OrganizationTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = OrganizationTypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "organization_type", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)

    @classmethod
    def get_organization_type(cls):
        ROOT_DIR = os.path.abspath(os.curdir)
        REL_PATH = "resources/PocketUserCredentialsandProperties.xlsx"
        FILE_PATH = os.path.join(ROOT_DIR, REL_PATH)
        user_id = 1
        username = "test"

        cls.delete_all()

        df = pd.read_excel(FILE_PATH, sheet_name="organization_type")
        file_data = df.values.tolist()

        for data in file_data:
            cls.add(user_id=user_id, user_name=username, name=data[1], description=data[2], subtype_id=data[3])
