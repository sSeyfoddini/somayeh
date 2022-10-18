from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.course_level_model import CourseLevelModel


class CourseLevelPersistence:
    @classmethod
    def add(cls, user_id, user_name, course_level):
        db.session.add(course_level)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CourseLevelModel.__tablename__,
                course_level.uuid,
                "INSERT",
                None,
                course_level._to_dict(),
            )
        )
        db.session.commit()
        return course_level

    @classmethod
    def update(cls, user_id, user_name, course_level):
        old_course_level = db.session.query(CourseLevelModel).get(course_level.uuid)
        if old_course_level is None:
            course_level = CourseLevelPersistence.add(user_id, user_name, course_level)
        else:
            old_course_level_clone = old_course_level._clone()
            old_course_level.name = course_level.name
            old_course_level.description = course_level.description
            old_course_level.type = course_level.type
            old_course_level.external_id = course_level.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CourseLevelModel.__tablename__,
                    course_level.uuid,
                    "UPDATE",
                    old_course_level_clone._to_dict(),
                    old_course_level._to_dict(),
                )
            )
            db.session.commit()
            course_level = old_course_level
        return course_level

    @classmethod
    def delete(cls, user_id, user_name, course_level):
        db.session.delete(course_level)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CourseLevelModel.__tablename__,
                course_level.uuid,
                "DELETE",
                course_level._to_dict(),
                None,
            )
        )

        db.session.commit()
        return course_level

    @classmethod
    def get(cls, uuid):
        return db.session.query(CourseLevelModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(CourseLevelModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(CourseLevelModel).filter_by(external_id=external_id)
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
                column = getattr(CourseLevelModel, key)
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
                    db.session.query(CourseLevelModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(CourseLevelModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(CourseLevelModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(CourseLevelModel).count()
        return result, total_records, page
