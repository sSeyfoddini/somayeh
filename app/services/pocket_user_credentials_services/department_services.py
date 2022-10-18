import logging
import os

import requests

from app.model.pocket_user_credentials_model.department_model import DepartmentModel
from app.persistence.pocket_user_credentials_persistence.department_persistence import DepartmentPersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class DepartmentService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        credential_type_id,
        department_id,
        department_label,
        date,
        type,
        external_id,
        parent_organization,
    ):

        department = DepartmentModel(
            credential_type_id=credential_type_id,
            department_id=department_id,
            department_label=department_label,
            date=date,
            type=type,
            external_id=external_id,
            parent_organization=parent_organization,
        )
        department = DepartmentPersistence.add(user_id, user_name, department)
        return department

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        department = DepartmentPersistence.get(uuid)

        if department is None:
            raise RecordNotFound("'department' with uuid '{}' not found.".format(uuid))

        department = DepartmentModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", department.credential_type_id),
            department_id=args.get("department_id", department.department_id),
            department_label=args.get("department_label", department.department_label),
            date=args.get("date", department.date),
            type=args.get("type", department.type),
            external_id=args.get("external_id", department.external_id),
            parent_organization=args.get("parent_organization", department.parent_organization)
        )
        department = DepartmentPersistence.update(user_id, user_name, department)

        return department

    @classmethod
    def delete_all(cls):
        DepartmentPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        department = DepartmentPersistence.get(uuid)
        if department is None:
            raise RecordNotFound("'department' with uuid '{}' not found.".format(uuid))
        DepartmentPersistence.delete(user_id, user_name, department)
        return department

    @classmethod
    def get(cls, uuid):
        department = DepartmentPersistence.get(uuid)
        if department is None:
            raise RecordNotFound("'department' with uuid '{}' not found.".format(uuid))
        return department

    @classmethod
    def get_all(cls):
        return DepartmentPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return DepartmentPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = DepartmentPersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "department", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
