from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.program_type_model import ProgramTypeModel


class ProgramTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, program_type):
        db.session.add(program_type)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ProgramTypeModel.__tablename__,
                program_type.uuid,
                "INSERT",
                None,
                program_type._to_dict(),
            )
        )
        db.session.commit()
        return program_type

    @classmethod
    def update(cls, user_id, user_name, program_type):
        old_program_type = db.session.query(ProgramTypeModel).filter_by(uuid=program_type.uuid).scalar()
        if old_program_type is None:
            program_type = ProgramTypePersistence.add(user_id, user_name, program_type)
        else:
            old_program_type_clone = old_program_type._clone()
            old_program_type.name = program_type.name
            old_program_type.description = program_type.description
            old_program_type.type = program_type.type
            old_program_type.external_id = program_type.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ProgramTypeModel.__tablename__,
                    program_type.uuid,
                    "UPDATE",
                    old_program_type_clone._to_dict(),
                    old_program_type._to_dict(),
                )
            )
            db.session.commit()
            program_type = old_program_type
        return program_type

    @classmethod
    def delete(cls, user_id, user_name, program_type):
        db.session.delete(program_type)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ProgramTypeModel.__tablename__,
                program_type.uuid,
                "DELETE",
                program_type._to_dict(),
                None,
            )
        )

        db.session.commit()
        return program_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(ProgramTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ProgramTypeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(ProgramTypeModel).filter_by(external_id=external_id)
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
                column = getattr(ProgramTypeModel, key)
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
                    db.session.query(ProgramTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ProgramTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ProgramTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ProgramTypeModel).count()
        return result, total_records, page