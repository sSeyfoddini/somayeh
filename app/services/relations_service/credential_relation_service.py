
from app.persistence.credential_relation_persistence import CredentialRelationPersistence, CredentialRelationModel
from app.util.error_handlers import RecordNotFound


class CredentialRelationService:
    @classmethod
    def add(cls, user_id, user_name, args):

        credential_relation = CredentialRelationModel(
            relation_type=args.get("relation_type"),
            target_cred_type_uuid=args.get("target_cred_type_uuid")
        )
        credential_relation = CredentialRelationPersistence.add(user_id, user_name, credential_relation)
        return credential_relation

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        credential_relation = CredentialRelationPersistence.get(uuid)

        if credential_relation is None:
            raise RecordNotFound("'credential relation' with uuid '{}' not found.".format(uuid))

        credential_relation = CredentialRelationModel(
            uuid=uuid,
            relation_type=args.get("relation_type", credential_relation.relation_type),
            target_cred_type_uuid=args.get("target_cred_type_uuid", credential_relation.target_cred_type_uuid)
        )
        credential_relation = CredentialRelationPersistence.update(user_id, user_name, credential_relation)

        return credential_relation

    @classmethod
    def delete_all(cls):
        CredentialRelationPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        credential_relation = CredentialRelationPersistence.get(uuid)
        if credential_relation is None:
            raise RecordNotFound("'credential relation' with uuid '{}' not found.".format(uuid))
        CredentialRelationPersistence.delete(user_id, user_name, credential_relation)
        return credential_relation

    @classmethod
    def get(cls, uuid):
        credential_relation = CredentialRelationPersistence.get(uuid)
        if credential_relation is None:
            raise RecordNotFound("'credential relation' with uuid '{}' not found.".format(uuid))
        return credential_relation

    @classmethod
    def get_all(cls):
        return CredentialRelationPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return CredentialRelationPersistence.get_all_by_filter(filter_dict)
