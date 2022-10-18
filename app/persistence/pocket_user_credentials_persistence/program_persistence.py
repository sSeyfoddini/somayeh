from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.program_model import ProgramModel


class ProgramPersistence:
    @classmethod
    def add(cls, user_id, user_name, program):
        db.session.add(program)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ProgramModel.__tablename__,
                program.uuid,
                "INSERT",
                None,
                program._to_dict(),
            )
        )

        db.session.commit()
        return program

    @classmethod
    def update(cls, user_id, user_name, program):
        old_program = db.session.query(ProgramModel).filter_by(uuid=program.uuid).scalar()
        if old_program is None:
            program = ProgramPersistence.add(user_id, user_name, program)
        else:
            old_program_clone = old_program._clone()
            old_program.credential_type_id = program.credential_type_id
            old_program.program_id = program.program_id
            old_program.program_label = program.program_label
            old_program.external_id = program.external_id
            old_program.program_type_label = program.program_type_label
            old_program.date = program.date
            old_program.type = program.type
            old_program.parent_organization = program.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ProgramModel.__tablename__,
                    program.uuid,
                    "UPDATE",
                    old_program_clone._to_dict(),
                    old_program._to_dict(),
                )
            )
            db.session.commit()
            program = old_program
        return program

    @classmethod
    def delete(cls, user_id, user_name, program):
        db.session.delete(program)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ProgramModel.__tablename__,
                program.uuid,
                "DELETE",
                program._to_dict(),
                None,
            )
        )
        db.session.commit()
        return program

    @classmethod
    def get(cls, uuid):
        return db.session.query(ProgramModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ProgramModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(ProgramModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(ProgramModel).delete()
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
                column = getattr(ProgramModel, key)
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
                    db.session.query(ProgramModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ProgramModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ProgramModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ProgramModel).count()
        return result, total_records, page
