import logging
import os

import pandas as pd
import requests

from app.model.pocket_user_credentials_model.organization_subtype_model import OrganizationSubtypeModel
from app.persistence.pocket_user_credentials_persistence.organization_subtype_persistence import (
    OrganizationSubtypePersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class OrganizationSubtypeService:
    @classmethod
    def add(cls, user_id, user_name, name, description, subtype_id):

        organization_subtype = OrganizationSubtypeModel(name=name, description=description, subtype_id=subtype_id)
        organization_subtype = OrganizationSubtypePersistence.add(user_id, user_name, organization_subtype)
        return organization_subtype

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        organization_subtype = OrganizationSubtypePersistence.get(uuid)

        if organization_subtype is None:
            raise RecordNotFound("'organization subtype' with uuid '{}' not found.".format(uuid))

        organization_subtype = OrganizationSubtypeModel(
            uuid=uuid,
            name=args.get("name", organization_subtype.name),
            description=args.get("description", organization_subtype.description),
            subtype_id=args.get("subtype_id", organization_subtype.subtype_id),
        )
        organization_subtype = OrganizationSubtypePersistence.update(user_id, user_name, organization_subtype)

        return organization_subtype

    @classmethod
    def delete_all(cls):
        OrganizationSubtypePersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        organization_subtype = OrganizationSubtypePersistence.get(uuid)
        if organization_subtype is None:
            raise RecordNotFound("'organization subtype' with uuid '{}' not found.".format(uuid))
        OrganizationSubtypePersistence.delete(user_id, user_name, organization_subtype)
        return organization_subtype

    @classmethod
    def get(cls, uuid):
        organization_subtype = OrganizationSubtypePersistence.get(uuid)
        if organization_subtype is None:
            raise RecordNotFound("'organization subtype' with uuid '{}' not found.".format(uuid))
        return organization_subtype

    @classmethod
    def get_all(cls):
        return OrganizationSubtypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return OrganizationSubtypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = OrganizationSubtypePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "organization_subtype", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)

    @classmethod
    def get_organization_subtype(cls):
        ROOT_DIR = os.path.abspath(os.curdir)
        REL_PATH = "resources/PocketUserCredentialsandProperties.xlsx"
        FILE_PATH = os.path.join(ROOT_DIR, REL_PATH)
        user_id = 1
        username = "test"

        cls.delete_all()

        df = pd.read_excel(FILE_PATH, sheet_name="organization_subtypes")
        file_data = df.values.tolist()

        for data in file_data:
            cls.add(user_id=user_id, user_name=username, name=data[2], description=data[3], subtype_id=data[1])
