from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.mime_type_model import MimeTypeModel


class MimeTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, mime_type):
        db.session.add(mime_type)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                MimeTypeModel.__tablename__,
                mime_type.uuid,
                "INSERT",
                None,
                mime_type._to_dict(),
            )
        )
        db.session.commit()
        return mime_type

    @classmethod
    def update(cls, user_id, user_name, mime_type):
        old_mime_type = db.session.query(MimeTypeModel).filter_by(uuid=mime_type.uuid).scalar()
        if old_mime_type is None:
            mime_type = MimeTypePersistence.add(user_id, user_name, mime_type)
        else:
            old_mime_type_clone = old_mime_type._clone()
            old_mime_type.mime_type1 = mime_type.mime_type1
            old_mime_type.extension = mime_type.extension
            old_mime_type.type = mime_type.type
            old_mime_type.external_id = mime_type.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    MimeTypeModel.__tablename__,
                    mime_type.uuid,
                    "UPDATE",
                    old_mime_type_clone._to_dict(),
                    old_mime_type._to_dict(),
                )
            )
            db.session.commit()
            mime_type = old_mime_type
        return mime_type

    @classmethod
    def delete(cls, user_id, user_name, mime_type):
        db.session.delete(mime_type)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                MimeTypeModel.__tablename__,
                mime_type.uuid,
                "DELETE",
                mime_type._to_dict(),
                None,
            )
        )
        db.session.commit()
        return mime_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(MimeTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(MimeTypeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(MimeTypeModel).filter_by(external_id=external_id)
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
                column = getattr(MimeTypeModel, key)
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
                    db.session.query(MimeTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(MimeTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(MimeTypeModel).filter(*queries).limit(limit).offset(
                (page - 1) * limit).all()

        total_records = db.session.query(MimeTypeModel).count()
        return result, total_records, page
