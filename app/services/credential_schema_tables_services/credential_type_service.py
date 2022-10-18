from uuid import uuid4

from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel
from app.persistence.credential_schema_tables_persistence.credential_type_persistence import CredentialTypePersistence
from app.util.error_handlers import RecordNotFound


class CredentialTypeService:
    @classmethod
    def add(cls, user_id, user_name, credential_definition_uuid, name, credential_type, schema_uri):

        credential_type = CredentialTypeModel(
            credential_definition_uuid=credential_definition_uuid,
            name=name,
            credential_type=credential_type,
            schema_uri=schema_uri,
        )
        credential_type = CredentialTypePersistence.add(user_id, user_name, credential_type)
        return credential_type

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        credential_type = CredentialTypePersistence.get(uuid)

        if credential_type is None:
            raise RecordNotFound("'credential type' with uuid '{}' not found.".format(uuid))

        credential_type = CredentialTypeModel(
            uuid=uuid,
            credential_definition_uuid=args.get("credential_definition_uuid", credential_type.credential_definition_uuid),
            name=args.get("name", credential_type.name),
            credential_type=args.get("credential_type", credential_type.credential_type),
            schema_uri=args.get("schema_uri", credential_type.schema_uri),
        )
        credential_type = CredentialTypePersistence.update(user_id, user_name, credential_type)

        return credential_type

    @classmethod
    def delete_all(cls):
        CredentialTypePersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        credential_type = CredentialTypePersistence.get(uuid)
        if credential_type is None:
            raise RecordNotFound("'credential type' with uuid '{}' not found.".format(uuid))
        CredentialTypePersistence.delete(user_id, user_name, credential_type)
        return credential_type

    @classmethod
    def get(cls, uuid):
        credential_type = CredentialTypePersistence.get(uuid)
        if credential_type is None:
            raise RecordNotFound("'credential type' with uuid '{}' not found.".format(uuid))
        return credential_type

    @classmethod
    def get_all(cls):
        return CredentialTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CredentialTypePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def insert(cls):
        user_id = 1
        user_name = "test"

        datas = []
        datas.extend(
            [
                CredentialTypeModel(
                    name="department",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="school",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="college",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="course",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="general_education_group_asu",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="organization_identity",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="program",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="role",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="term",
                    uuid=str(uuid4())
                ),
                CredentialTypeModel(
                    name="title",
                    uuid=str(uuid4())
                ),
            ]
        )

        for data in datas:
            CredentialTypePersistence.add(user_id, user_name, data)
