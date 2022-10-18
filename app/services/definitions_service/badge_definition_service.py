from uuid import uuid4

from app.model.definitions_model.badge_definition_model import BadgeDefinitionModel
from app.persistence.definitions_persistence.badge_definition_persistence import BadgeDefinitionPersistence
from app.util.error_handlers import RecordNotFound

class BadgeDefinitionService:
    @classmethod
    def add(cls, user_id, user_name, badge_id, badge_name):

        badge_definition = BadgeDefinitionModel(uuid=str(uuid4()), badge_id=badge_id, badge_name=badge_name)
        badge_definition = BadgeDefinitionPersistence.add(user_id, user_name, badge_definition)
        return badge_definition

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        badge_definition = BadgeDefinitionPersistence.get(uuid)

        if badge_definition is None:
            raise RecordNotFound("'badge definition' with uuid'{}' not found.".format(uuid))

        badge_definition = BadgeDefinitionModel(
            uuid=uuid,
            badge_id=args.get("badge_id", badge_definition.badge_id),
            badge_name=args.get("badge_name", badge_definition.badge_name),


        )


        badge_definition = args.get(BadgeDefinitionPersistence.update(user_id, user_name, badge_definition))

        return badge_definition

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        badge_definition = BadgeDefinitionPersistence.get(uuid)
        if badge_definition is None:
            raise RecordNotFound("'badge definition' with uuid'{}' not found.".format(uuid))
        BadgeDefinitionPersistence.delete(user_id, user_name, badge_definition)
        return badge_definition

    @classmethod
    def get(cls, uuid):
        badge_definition = BadgeDefinitionPersistence.get(uuid)
        if badge_definition is None:
            raise RecordNotFound("'badge definition' with uuid'{}' not found.".format(uuid))
        return badge_definition

    @classmethod
    def get_all(cls):
        return BadgeDefinitionPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return BadgeDefinitionPersistence.get_all_by_filter(filter_dict)

