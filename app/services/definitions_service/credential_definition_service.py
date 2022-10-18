
from app.persistence.credential_definition_persistence import CredentialDefinitionModel, CredentialDefinitionPersistence
from app.util.error_handlers import RecordNotFound


class CredentialDefinitionService:
    @classmethod
    def add(cls, user_id, user_name, args):

        credential_definition = CredentialDefinitionModel(
            cred_def_type=args.get("cred_def_type"),
            cred_def=args.get("cred_def"),
            schema=args.get("schema"),
            name=args.get("name")
        )
        credential_definition = CredentialDefinitionPersistence.add(user_id, user_name, credential_definition)
        return credential_definition

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        credential_definition = CredentialDefinitionPersistence.get(uuid)

        if credential_definition is None:
            raise RecordNotFound("'credential definition' with uuid '{}' not found.".format(uuid))

        credential_definition = CredentialDefinitionModel(
            uuid=uuid,
            cred_def_type=args.get("cred_def_type", credential_definition.cred_def_type),
            cred_def=args.get("cred_def", credential_definition.cred_def),
            schema=args.get("schema", credential_definition.schema),
            name=args.get("name", credential_definition.name)
        )
        credential_definition = CredentialDefinitionPersistence.update(user_id, user_name, credential_definition)

        return credential_definition

    @classmethod
    def delete_all(cls):
        CredentialDefinitionPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        credential_definition = CredentialDefinitionPersistence.get(uuid)
        if credential_definition is None:
            raise RecordNotFound("'credential definition' with uuid '{}' not found.".format(uuid))
        CredentialDefinitionPersistence.delete(user_id, user_name, credential_definition)
        return credential_definition

    @classmethod
    def get(cls, uuid):
        credential_definition = CredentialDefinitionPersistence.get(uuid)
        if credential_definition is None:
            raise RecordNotFound("'credential definition' with uuid '{}' not found.".format(uuid))
        return credential_definition

    @classmethod
    def get_all(cls):
        return CredentialDefinitionPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CredentialDefinitionPersistence.get_all_by_filter(filter_dict)
