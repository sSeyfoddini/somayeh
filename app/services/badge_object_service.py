
from app.persistence.badge_object_persistence import BadgeObjectModel, BadgeObjectPersistence
from app.util.error_handlers import RecordNotFound


class BadgeObjectService:
    @classmethod
    def add(cls, user_id, user_name, args):

        badge_object = BadgeObjectModel(
            badge_def_uuid=args.get("badge_def_uuid"),
            learner_uuid=args.get("learner_uuid"),
            status=args.get("status"),
        )
        badge_object = BadgeObjectPersistence.add(user_id, user_name, badge_object)
        return badge_object

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        badge_object = BadgeObjectPersistence.get(uuid)

        if badge_object is None:
            raise RecordNotFound("'badge object' with uuid '{}' not found.".format(uuid))

        badge_object = BadgeObjectModel(
            uuid=uuid,
            badge_def_uuid=args.get("badge_def_uuid", badge_object.badge_def_uuid),
            learner_uuid=args.get("learner_uuid", badge_object.learner_uuid),
            status = args.get("status", badge_object.status),
        )
        badge_object = BadgeObjectPersistence.update(user_id, user_name, badge_object)

        return badge_object

    @classmethod
    def delete_all(cls):
        BadgeObjectPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        badge_object = BadgeObjectPersistence.get(uuid)
        if badge_object is None:
            raise RecordNotFound("'badge object' with uuid '{}' not found.".format(uuid))
        BadgeObjectPersistence.delete(user_id, user_name, badge_object)
        return badge_object

    @classmethod
    def get(cls, uuid):
        badge_object = BadgeObjectPersistence.get(uuid)
        if badge_object is None:
            raise RecordNotFound("'badge object' with uuid '{}' not found.".format(uuid))
        return badge_object

    @classmethod
    def get_all(cls):
        return BadgeObjectPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return BadgeObjectPersistence.get_all_by_filter(filter_dict)
