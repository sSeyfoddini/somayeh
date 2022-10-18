from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.grade_model import GradeModel


class GradePersistence:
    @classmethod
    def add(cls, user_id, user_name, grade):
        db.session.add(grade)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GradeModel.__tablename__,
                grade.uuid,
                "INSERT",
                None,
                grade._to_dict(),
            )
        )
        db.session.commit()
        return grade

    @classmethod
    def update(cls, user_id, user_name, grade):
        old_grade = db.session.query(GradeModel).filter_by(uuid=grade.uuid).scalar()
        if old_grade is None:
            grade = GradePersistence.add(user_id, user_name, grade)
        else:
            old_grade_clone = old_grade._clone()
            old_grade.letter = grade.letter
            old_grade.value = grade.value
            old_grade.description = grade.description
            old_grade.type = grade.type
            old_grade.external_id = grade.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    GradeModel.__tablename__,
                    grade.uuid,
                    "UPDATE",
                    old_grade_clone._to_dict(),
                    old_grade._to_dict(),
                )
            )
            db.session.commit()
            grade = old_grade
        return grade

    @classmethod
    def delete(cls, user_id, user_name, grade):
        db.session.delete(grade)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GradeModel.__tablename__,
                grade.id,
                "DELETE",
                grade._to_dict(),
                None,
            )
        )

        db.session.commit()
        return grade

    @classmethod
    def get(cls, uuid):
        return db.session.query(GradeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(GradeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(GradeModel).filter_by(external_id=external_id)
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
                column = getattr(GradeModel, key)
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
                    db.session.query(GradeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(GradeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(GradeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(GradeModel).count()
        return result, total_records, page