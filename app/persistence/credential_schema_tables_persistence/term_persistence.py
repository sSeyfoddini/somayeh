from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.term_model import TermModel


class TermPersistence:
    @classmethod
    def add(cls, user_id, user_name, term):
        db.session.add(term)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                TermModel.__tablename__,
                term.uuid,
                "INSERT",
                None,
                term._to_dict(),
            )
        )
        db.session.commit()
        return term

    @classmethod
    def update(cls, user_id, user_name, term):
        old_term = db.session.query(TermModel).filter_by(uuid=term.uuid).scalar()
        if old_term is None:
            term = TermPersistence.add(user_id, user_name, term)
        else:
            old_term_clone = old_term._clone()
            old_term.name = term.name
            old_term.start_date = term.start_date
            old_term.end_date = term.end_date
            old_term.session_id = term.session_id
            old_term.type = term.type
            old_term.external_id = term.external_id
            old_term.credential_type_id = term.credential_type_id
            old_term.parent_organization = term.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    TermModel.__tablename__,
                    term.uuid,
                    "UPDATE",
                    old_term_clone._to_dict(),
                    old_term._to_dict(),
                )
            )
            db.session.commit()
            term = old_term
        return term

    @classmethod
    def delete(cls, user_id, user_name, term):
        db.session.delete(term)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                TermModel.__tablename__,
                term.uuid,
                "DELETE",
                term._to_dict(),
                None,
            )
        )

        db.session.commit()
        return term

    @classmethod
    def get(cls, uuid):
        return db.session.query(TermModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(TermModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(TermModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(TermModel).delete()
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
                column = getattr(TermModel, key)
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
                    db.session.query(TermModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(TermModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(TermModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(TermModel).count()
        return result, total_records, page
