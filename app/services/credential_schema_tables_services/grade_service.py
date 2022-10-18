import logging
import os

import requests

from app.model.credential_schema_tables_model.grade_model import GradeModel
from app.persistence.credential_schema_tables_persistence.grade_persistence import GradePersistence
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class GradeService:
    @classmethod
    def add(cls, user_id, user_name, letter, value, description, type, external_id):

        grade = GradeModel(
            letter=letter,
            value=value,
            description=description,
            type=type,
            external_id=external_id,
        )
        grade = GradePersistence.add(user_id, user_name, grade)
        return grade

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        grade = GradePersistence.get(uuid)

        if grade is None:
            raise RecordNotFound("'grade' with uuid '{}' not found.".format(uuid))

        grade = GradeModel(
            uuid=uuid,
            letter=args.get("letter", grade.letter),
            value=args.get("value", grade.value),
            description=args.get("description", grade.description),
            type=args.get("type", grade.type),
            external_id=args.get("external_id", grade.external_id),
        )
        grade = GradePersistence.update(user_id, user_name, grade)

        return grade

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        grade = GradePersistence.get(uuid)
        if grade is None:
            raise RecordNotFound("'grade' with uuid '{}' not found.".format(uuid))
        GradePersistence.delete(user_id, user_name, grade)
        return grade

    @classmethod
    def get(cls, uuid):
        grade = GradePersistence.get(uuid)
        if grade is None:
            raise RecordNotFound("'grade' with uuid '{}' not found.".format(uuid))
        return grade

    @classmethod
    def get_all(cls):
        return GradePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return GradePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = GradePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "grade", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
