
from app import db

from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.model.pocket_user_credentials_model.title_model import TitleModel
from app.persistence.pocket_user_credentials_persistence.title_persistence import TitlePersistence
from app.services.thin_client_service import EmployeeService



class Title:
    @classmethod
    def update(cls, limit):
        user_id = 1
        user_name = "test"
        input = {"emplid": "1900000003"}
        page = 1

        responses = []

        while True:
            response = EmployeeService.get(input, page, limit)
            if not response:
                break
            responses.append(response)
            page = page + 1

        db.session.query(TitleModel).delete()

        credential_type_id = (
            db.session.query(CredentialTypeModel.uuid).filter(CredentialTypeModel.name == "title").scalar()
        )
        for response in responses:
            for data in response:

                title = TitleModel(
                    credential_type_id=credential_type_id,
                    credential_type_label="",
                    title_type_id=data["title_type_id"],
                    title_type_label=data["title_type_name"],
                    organization_id=data["organization_id"],
                    organization_label=data["organization_name"],
                    conferral_date=data["conferral_date"],
                    type="",
                    external_id="",
                )
                TitlePersistence.add(user_id, user_name, title)


