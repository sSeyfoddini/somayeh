
from app.model.role_model import RoleModel
from app.persistence.role_persistence import RolePersistence
from app.util.error_handlers import RecordNotFound


class RoleService:
    @classmethod
    def add(cls, user_id, user_name, args):

        role = RoleModel(
            name=args.get("name"),
            type=args.get("type"),
            external_id=args.get("external_id"),
            credential_type_id=args.get("credential_type_id"),
            parent_organization=args.get("parent_organization"),
        )
        role = RolePersistence.add(user_id, user_name, role)
        return role

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        role = RolePersistence.get(uuid)

        if role is None:
            raise RecordNotFound("'role' with uuid '{}' not found.".format(uuid))

        role = RoleModel(
            uuid=uuid,
            name=args.get("name", role.name),
            type=args.get("type", role.type),
            external_id=args.get("external_id", role.external_id),
            credential_type_id=args.get("credential_type_id", role.credential_type_id),
            parent_organization=args.get("parent_organization", role.parent_organization),
        )
        role = RolePersistence.update(user_id, user_name, role)

        return role

    @classmethod
    def delete_all(cls):
        RolePersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        role = RolePersistence.get(uuid)
        if role is None:
            raise RecordNotFound("'role' with uuid '{}' not found.".format(uuid))

        RolePersistence.delete(user_id, user_name, role)
        return role

    @classmethod
    def get(cls, uuid):
        role = RolePersistence.get(uuid)
        if role is None:
            raise RecordNotFound("'role' with uuid '{}' not found.".format(uuid))
        return role

    @classmethod
    def get_all(cls):
        return RolePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return RolePersistence.get_all_by_filter(filter_dict)
