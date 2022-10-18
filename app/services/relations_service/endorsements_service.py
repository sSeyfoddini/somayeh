from app.model.relations_model.endorsements_model import EndorsementsModel
from app.persistence.relations_persistence.endorsements_persistence import EndorsementsPersistence
from app.util.error_handlers import RecordNotFound

class EndorsementsService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        endorsement_type_id,
        endorsement_name,
        endorsement_category_id,
        endorsement_keywords,
        conferring_credential,
        conferring_identifier,
        supporting_credential,
    ):

        endorsement = EndorsementsModel(
            endorsement_type_id=endorsement_type_id,
            endorsement_name=endorsement_name,
            endorsement_category_id=endorsement_category_id,
            endorsement_keywords=endorsement_keywords,
            conferring_credential=conferring_credential,
            conferring_identifier=conferring_identifier,
            supporting_credential=supporting_credential,
        )
        endorsement = EndorsementsPersistence.add(user_id, user_name, endorsement)
        return endorsement

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        id,
        args
    ):
        endorsement = EndorsementsPersistence.get(id)

        if endorsement is None:
            raise RecordNotFound("'endorsement' with id'{}' not found.".format(id))

        endorsement = EndorsementsModel(
            id=id,
            endorsement_type_id=args.get("endorsement_type_id", endorsement.endorsement_type_id),
            endorsement_name=args.get("endorsement_name", endorsement.endorsement_name),
            endorsement_category_id=args.get("endorsement_category_id", endorsement.endorsement_category_id),
            endorsement_keywords=args.get("endorsement_keywords", endorsement.endorsement_keywords),
            conferring_credential=args.get("conferring_credential", endorsement.conferring_credential),
            conferring_identifier=args.get("conferring_identifier", endorsement.conferring_identifier),
            supporting_credential=args.get("supporting_credential", endorsement.supporting_credential),
        )
        endorsement = EndorsementsPersistence.update(user_id, user_name, endorsement)

        return endorsement

    @classmethod
    def delete(cls, user_id, user_name, endorsement):
        EndorsementsPersistence.delete(user_id, user_name, endorsement)
        return endorsement

    @classmethod
    def delete_by_id(cls, user_id, user_name, id):
        endorsement = EndorsementsPersistence.get(id)
        if endorsement is None:
            raise RecordNotFound("'endorsement' with id'{}' not found.".format(id))
        EndorsementsPersistence.delete(user_id, user_name, endorsement)
        return endorsement

    @classmethod
    def get(cls, id):
        endorsement = EndorsementsPersistence.get(id)
        if endorsement is None:
            raise RecordNotFound("'endorsement' with id'{}' not found.".format(id))
        return endorsement

    @classmethod
    def get_all(cls, page, limit):
        return EndorsementsPersistence.get_all(page, limit)
