from uuid import uuid4

from app import db

# from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
# from app.model.pocket_user_credentials_model.college_model import CollegeModel
# from app.persistence.pocket_user_credentials_persistence.college_persistence import CollegePersistence
from app.services.thin_client_service import CollegesService


class Colleges:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        parent_organization = "ASU"
        input = {"term_code": "2221"}
        page = 1

        responses = []
        while True:
            response = CollegesService.get(input, page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        """delete = db.session.query(CollegeModel).delete()

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid).filter(CredentialTypeModel.name == "college").scalar()
        )
        for response in responses:
            for data in response:
                college = CollegeModel(
                    credential_type_id=credential_type_id,
                    college_id=data["college_id"] if "college_id" in data else "",
                    college_label=data["name"] if "name" in data else "",
                    date=data["date"] if "date" in data else None,
                    type=data["type"] if "type" in data else "",
                    external_id=data["external_id"] if "external_id" in data else "",
                    parent_organization=parent_organization,
                    uuid=str(uuid4()),
                )
                college = CollegePersistence.add(user_id, user_name, college)"""
