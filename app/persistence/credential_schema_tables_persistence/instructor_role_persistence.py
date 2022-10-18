from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.instructor_role_model import InstructorRoleModel


class InstructorRolePersistence:
    @classmethod
    def add(cls, user_id, user_name, instructor_role):
        db.session.add(instructor_role)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                InstructorRoleModel.__tablename__,
                instructor_role.uuid,
                "INSERT",
                None,
                instructor_role._to_dict(),
            )
        )
        db.session.commit()
        return instructor_role

    @classmethod
    def update(cls, user_id, user_name, instructor_role):
        old_instructor_role = db.session.query(InstructorRoleModel).filter_by(uuid=instructor_role.uuid).scalar()
        if old_instructor_role is None:
            instructor_role = InstructorRolePersistence.add(user_id, user_name, instructor_role)
        else:
            old_instructor_role_clone = old_instructor_role._clone()
            old_instructor_role.name = instructor_role.name
            old_instructor_role.description = instructor_role.description
            old_instructor_role.type = instructor_role.type
            old_instructor_role.external_id = instructor_role.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    InstructorRoleModel.__tablename__,
                    instructor_role.uuid,
                    "UPDATE",
                    old_instructor_role_clone._to_dict(),
                    old_instructor_role._to_dict(),
                )
            )
            db.session.commit()
            instructor_role = old_instructor_role
        return instructor_role

    @classmethod
    def delete(cls, user_id, user_name, instructor_role):
        db.session.delete(instructor_role)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                InstructorRoleModel.__tablename__,
                instructor_role.uuid,
                "DELETE",
                instructor_role._to_dict(),
                None,
            )
        )

        db.session.commit()
        return instructor_role

    @classmethod
    def get(cls, uuid):
        return db.session.query(InstructorRoleModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(InstructorRoleModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(InstructorRoleModel).filter_by(external_id=external_id)
        return result.all()

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
                column = getattr(InstructorRoleModel, key)
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
                    db.session.query(InstructorRoleModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(InstructorRoleModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(InstructorRoleModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(InstructorRoleModel).count()
        return result, total_records, page