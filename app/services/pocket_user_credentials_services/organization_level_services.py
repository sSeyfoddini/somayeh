import os
import pandas as pd

from app.model.pocket_user_credentials_model.organization_level_model import OrganizationLevelModel
from app.persistence.pocket_user_credentials_persistence.organization_level_persistence import (
    OrganizationLevelPersistence,
)
from app.util.error_handlers import RecordNotFound


class OrganizationLevelService:
    @classmethod
    def add(cls, user_id, user_name, name, description):

        organization_level = OrganizationLevelModel(name=name, description=description)
        organization_level = OrganizationLevelPersistence.add(user_id, user_name, organization_level)
        return organization_level

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        organization_level = OrganizationLevelPersistence.get(uuid)

        if organization_level is None:
            raise RecordNotFound("'organization level' with uuid '{}' not found.".format(uuid))

        organization_level = OrganizationLevelModel(
            uuid=uuid,
            name=args.get("name",organization_level.name),
            description=args.get("description", organization_level.description)
        )
        organization_level = OrganizationLevelPersistence.update(user_id, user_name, organization_level)

        return organization_level

    @classmethod
    def delete_all(cls):
        OrganizationLevelPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        organization_level = OrganizationLevelPersistence.get(uuid)
        if organization_level is None:
            raise RecordNotFound("'organization level' with uuid '{}' not found.".format(uuid))
        OrganizationLevelPersistence.delete(user_id, user_name, organization_level)
        return organization_level

    @classmethod
    def get(cls, uuid):
        organization_level = OrganizationLevelPersistence.get(uuid)
        if organization_level is None:
            raise RecordNotFound("'organization level' with uuid '{}' not found.".format(uuid))
        return organization_level

    @classmethod
    def get_all(cls):
        return OrganizationLevelPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return OrganizationLevelPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def get_organization_level(cls):
        ROOT_DIR = os.path.abspath(os.curdir)
        REL_PATH = "resources/PocketUserCredentialsandProperties.xlsx"
        FILE_PATH = os.path.join(ROOT_DIR, REL_PATH)
        user_id = 1
        username = "test"

        cls.delete_all()

        df = pd.read_excel(FILE_PATH, sheet_name="organization_level")
        file_data = df.values.tolist()

        for data in file_data:
            cls.add(
                user_id=user_id,
                user_name=username,
                name=data[1],
                description=data[2],
            )
