from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.role_model import RoleModel


class RolePersistence:
    @classmethod
    def add(cls, user_id, user_name, role):
        db.session.add(role)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                RoleModel.__tablename__,
                role.uuid,
                "INSERT",
                None,
                role._to_dict(),
            )
        )
        db.session.commit()
        return role

    @classmethod
    def update(cls, user_id, user_name, role):
        old_role = db.session.query(RoleModel).filter_by(uuid=role.uuid).scalar()
        if old_role is None:
            role = RolePersistence.add(user_id, user_name, role)
        else:
            old_role_clone = old_role._clone()
            old_role.name = role.name
            old_role.type = role.type
            old_role.external_id = role.external_id
            old_role.credential_type_id = role.credential_type_id
            old_role.parent_organization = role.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    RoleModel.__tablename__,
                    role.uuid,
                    "UPDATE",
                    old_role_clone._to_dict(),
                    old_role._to_dict(),
                )
            )
            db.session.commit()
            role = old_role
        return role

    @classmethod
    def delete(cls, user_id, user_name, role):
        db.session.delete(role)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                RoleModel.__tablename__,
                role.uuid,
                "DELETE",
                role._to_dict(),
                None,
            )
        )
        db.session.commit()
        return role

    @classmethod
    def get(cls, uuid):
        return db.session.query(RoleModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(RoleModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(RoleModel).delete()
        db.session.commit()

    @classmethod
    def get_all_by_filter(
            cls,
            filter_list
    ):
        page = 1
        limit = 10
        sort = None
        queries = []
        for key, val in filter_list.items():
            if key == "page":
                page = int(val)
            elif key == "limit":
                limit = int(val)
            elif key == "sort":
                sort = val
            else:
                column = getattr(RoleModel, key)
                if key == "uuid":
                    queries.append(func.lower(column) == func.lower(val))
                elif column.type.python_type == str:
                    queries.append(func.lower(column).contains(func.lower(val)))
                elif column.type.python_type == int or column.type.python_type == float \
                    or column.type.python_type == bool or column.type.python_type == datetime:
                    queries.append(column == val)
                else:
                    queries.append(column.contains(val))

        if sort:
            sort_column, sort_method = sort.split(":", 1)
            if sort_method == "desc":
                result = (
                    db.session.query(RoleModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(RoleModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(RoleModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(RoleModel).count()
        return result, total_records, page