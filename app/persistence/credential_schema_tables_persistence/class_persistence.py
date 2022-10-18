from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.class_model import ClassModel


class ClassPersistence:
    @classmethod
    def add(cls, user_id, user_name, given_class):
        db.session.add(given_class)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ClassModel.__tablename__,
                given_class.uuid,
                "INSERT",
                None,
                given_class._to_dict(),
            )
        )
        db.session.commit()
        return given_class

    @classmethod
    def update(cls, user_id, user_name, given_class):
        old_given_class = db.session.query(ClassModel).filter_by(uuid=given_class.uuid).scalar()
        if old_given_class is None:
            given_class = ClassPersistence.add(user_id, user_name, given_class)
        else:
            old_given_class_clone = given_class._clone()
            old_given_class.external_class_id = given_class.external_class_id
            old_given_class.course_id = given_class.course_id
            old_given_class.external_course_id = given_class.external_course_id
            old_given_class.instructor_id = given_class.instructor_id
            old_given_class.session_id = given_class.session_id
            old_given_class.term_id = given_class.term_id
            old_given_class.topic = given_class.topic
            old_given_class.reference_uri = given_class.reference_uri
            old_given_class.delivery_id = given_class.delivery_id
            old_given_class.location_id = given_class.location_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ClassModel.__tablename__,
                    given_class.uuid,
                    "UPDATE",
                    old_given_class_clone._to_dict(),
                    old_given_class._to_dict(),
                )
            )
            db.session.commit()
            given_class = old_given_class
        return given_class

    @classmethod
    def delete(cls, user_id, user_name, given_class):
        db.session.delete(given_class)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ClassModel.__tablename__,
                given_class.uuid,
                "DELETE",
                given_class._to_dict(),
                None,
            )
        )

        db.session.commit()
        return given_class

    @classmethod
    def delete_all(cls):
        db.session.query(ClassModel).delete()
        db.session.commit()

    @classmethod
    def get(cls, uuid):
        return db.session.query(ClassModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ClassModel).all()
    
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
                column = getattr(ClassModel, key)
                if key == "uuid":
                    queries.append(func.lower(column) == func.lower(val))
                elif column.type.python_type == str:
                    queries.append(func.lower(column).contains(func.lower(val)))
                else:
                    queries.append(val in column)
        if sort:
            sort_column, sort_method = sort.split(":", 1)
            if sort_method == "desc":
                result = (
                    db.session.query(ClassModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ClassModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ClassModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ClassModel).count()
        return result, total_records, page
