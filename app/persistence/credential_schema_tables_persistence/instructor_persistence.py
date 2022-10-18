from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.instructor_model import InstructorModel


class InstructorPersistence:
    @classmethod
    def add(cls, user_id, user_name, instructor):
        db.session.add(instructor)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                InstructorModel.__tablename__,
                instructor.uuid,
                "INSERT",
                None,
                instructor._to_dict(),
            )
        )
        db.session.commit()
        return instructor

    @classmethod
    def update(cls, user_id, user_name, instructor):
        old_instructor = db.session.query(InstructorModel).filter_by(uuid=instructor.uuid).scalar()
        if old_instructor is None:
            instructor = InstructorPersistence.add(user_id, user_name, instructor)
        else:
            old_instructor_clone = old_instructor._clone()
            old_instructor.name = instructor.name
            old_instructor.school_id = instructor.school_id
            old_instructor.college_id = instructor.college_id
            old_instructor.instructor_role_id = instructor.instructor_role_id
            old_instructor.did = instructor.did
            old_instructor.reference_uri = instructor.reference_uri
            old_instructor.type = instructor.type
            old_instructor.external_id = instructor.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    InstructorModel.__tablename__,
                    instructor.uuid,
                    "UPDATE",
                    old_instructor_clone._to_dict(),
                    old_instructor._to_dict(),
                )
            )
            db.session.commit()
            instructor = old_instructor
        return instructor

    @classmethod
    def delete(cls, user_id, user_name, instructor):
        db.session.delete(instructor)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                InstructorModel.__tablename__,
                instructor.uuid,
                "DELETE",
                instructor._to_dict(),
                None,
            )
        )

        db.session.commit()
        return instructor

    @classmethod
    def get(cls, uuid):
        return db.session.query(InstructorModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(InstructorModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(InstructorModel).filter_by(external_id=external_id)
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
                column = getattr(InstructorModel, key)
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
                    db.session.query(InstructorModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(InstructorModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(InstructorModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(InstructorModel).count()
        return result, total_records, page