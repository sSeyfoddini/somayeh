from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.definitions_model.class_enrollment_definition_model import ClassEnrollmentDefinitionModel


class ClassEnrollmentDefinitionPersistence:
    @classmethod
    def add(cls, user_id, user_name, class_enrollment):
        db.session.add(class_enrollment)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ClassEnrollmentDefinitionModel.__tablename__,
                class_enrollment.uuid,
                "INSERT",
                None,
                class_enrollment._to_dict(),
            )
        )
        db.session.commit()
        return class_enrollment

    @classmethod
    def update(cls, user_id, user_name, class_enrollment):
        old_class_enrollment = (
            db.session.query(ClassEnrollmentDefinitionModel).filter_by(uuid=class_enrollment.uuid).scalar()
        )
        if old_class_enrollment is None:
            class_enrollment = ClassEnrollmentDefinitionPersistence.add(user_id, user_name, class_enrollment)
        else:
            old_class_enrollment_clone = old_class_enrollment._clone()
            old_class_enrollment.course_id = class_enrollment.course_id
            old_class_enrollment.course_subject = class_enrollment.course_subject
            old_class_enrollment.course_number = class_enrollment.course_number
            old_class_enrollment.course_name = class_enrollment.course_name

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ClassEnrollmentDefinitionModel.__tablename__,
                    class_enrollment.uuid,
                    "UPDATE",
                    old_class_enrollment_clone._to_dict(),
                    old_class_enrollment._to_dict(),
                )
            )
            db.session.commit()
            class_enrollment = old_class_enrollment
        return class_enrollment

    @classmethod
    def delete(cls, user_id, user_name, class_enrollment):
        db.session.delete(class_enrollment)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ClassEnrollmentDefinitionModel.__tablename__,
                class_enrollment.uuid,
                "DELETE",
                class_enrollment._to_dict(),
                None,
            )
        )
        db.session.commit()
        return class_enrollment

    @classmethod
    def get(cls, uuid):
        return db.session.query(ClassEnrollmentDefinitionModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ClassEnrollmentDefinitionModel).all()

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
                column = getattr(ClassEnrollmentDefinitionModel, key)
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
                    db.session.query(ClassEnrollmentDefinitionModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ClassEnrollmentDefinitionModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ClassEnrollmentDefinitionModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ClassEnrollmentDefinitionModel).count()
        return result, total_records, page