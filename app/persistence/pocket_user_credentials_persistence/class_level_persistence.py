from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.class_level_model import ClassLevelModel


class ClassLevelPersistence:
    @classmethod
    def add(cls, user_id, user_name, class_level):
        db.session.add(class_level)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ClassLevelModel.__tablename__,
                class_level.uuid,
                "INSERT",
                None,
                class_level._to_dict(),
            )
        )
        db.session.commit()
        return class_level

    @classmethod
    def update(cls, user_id, user_name, class_level):
        old_class_level = db.session.query(ClassLevelModel).filter_by(uuid=class_level.uuid).scalar()
        if old_class_level is None:
            class_level = ClassLevelPersistence.add(user_id, user_name, class_level)
        else:
            old_class_level_clone = old_class_level._clone()
            old_class_level.level = class_level.level
            old_class_level.description = class_level.description
            old_class_level.semester_order = class_level.semester_order
            old_class_level.type = class_level.type
            old_class_level.external_id = class_level.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ClassLevelModel.__tablename__,
                    class_level.uuid,
                    "UPDATE",
                    old_class_level_clone._to_dict(),
                    old_class_level._to_dict(),
                )
            )
            db.session.commit()
            class_level = old_class_level
        return class_level

    @classmethod
    def delete(cls, user_id, user_name, class_level):
        db.session.delete(class_level)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ClassLevelModel.__tablename__,
                class_level.uuid,
                "DELETE",
                class_level._to_dict(),
                None,
            )
        )
        db.session.commit()
        return class_level

    @classmethod
    def get(cls, uuid):
        return db.session.query(ClassLevelModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ClassLevelModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(ClassLevelModel).filter_by(external_id=external_id)
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
                column = getattr(ClassLevelModel, key)
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
                    db.session.query(ClassLevelModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ClassLevelModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ClassLevelModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ClassLevelModel).count()
        return result, total_records, page