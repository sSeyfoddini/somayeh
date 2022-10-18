from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.program_completion_model import ProgramCompletionModel


class ProgramCompletionPersistence:
    @classmethod
    def add(cls, user_id, user_name, program_completion):
        db.session.add(program_completion)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ProgramCompletionModel.__tablename__,
                program_completion.uuid,
                "INSERT",
                None,
                program_completion._to_dict(),
            )
        )
        db.session.commit()
        return program_completion

    @classmethod
    def update(cls, user_id, user_name, program_completion):
        old_program_completion = db.session.query(ProgramCompletionModel).filter_by(uuid=program_completion.uuid).scalar()
        if old_program_completion is None:
            program_completion = ProgramCompletionPersistence.add(user_id, user_name, program_completion)
        else:
            old_program_completion_clone = old_program_completion._clone()
            old_program_completion.credential_type_id = program_completion.credential_type_id
            old_program_completion.credential_type_label = program_completion.credential_type_label
            old_program_completion.recognition_date = program_completion.recognition_date
            old_program_completion.term_id = program_completion.term_id
            old_program_completion.term_label = program_completion.term_label
            old_program_completion.program_id = program_completion.program_id
            old_program_completion.program_label = program_completion.program_label
            old_program_completion.credential_label = program_completion.credential_label
            old_program_completion.type = program_completion.type
            old_program_completion.external_id = program_completion.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ProgramCompletionModel.__tablename__,
                    program_completion.uuid,
                    "UPDATE",
                    old_program_completion_clone._to_dict(),
                    old_program_completion._to_dict(),
                )
            )
            db.session.commit()
            program_completion = old_program_completion
        return program_completion

    @classmethod
    def delete(cls, user_id, user_name, program_completion):
        db.session.delete(program_completion)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ProgramCompletionModel.__tablename__,
                program_completion.uuid,
                "DELETE",
                program_completion._to_dict(),
                None,
            )
        )

        db.session.commit()
        return program_completion

    @classmethod
    def get(cls, uuid):
        return db.session.query(ProgramCompletionModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ProgramCompletionModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(ProgramCompletionModel).filter_by(external_id=external_id)
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
                column = getattr(ProgramCompletionModel, key)
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
                    db.session.query(ProgramCompletionModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ProgramCompletionModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ProgramCompletionModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ProgramCompletionModel).count()
        return result, total_records, page