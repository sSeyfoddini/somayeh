from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.title_type_model import TitleTypeModel


class TitleTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, title_type):
        db.session.add(title_type)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                TitleTypeModel.__tablename__,
                title_type.uuid,
                "INSERT",
                None,
                title_type._to_dict(),
            )
        )

        db.session.commit()
        return title_type

    @classmethod
    def update(cls, user_id, user_name, title_type):
        old_title_type = db.session.query(TitleTypeModel).filter_by(uuid=title_type.uuid).scalar()
        if old_title_type is None:
            title_type = TitleTypePersistence.add(user_id, user_name, title_type)
        else:
            old_title_type_clone = old_title_type._clone()
            old_title_type.name = title_type.name
            old_title_type.description = title_type.description
            old_title_type.reference_url = title_type.reference_url
            old_title_type.type = title_type.type
            old_title_type.external_id = title_type.external_id
            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    TitleTypeModel.__tablename__,
                    title_type.uuid,
                    "UPDATE",
                    old_title_type_clone._to_dict(),
                    old_title_type._to_dict(),
                )
            )
            db.session.commit()
            title_type = old_title_type
        return title_type

    @classmethod
    def delete(cls, user_id, user_name, title_type):
        db.session.delete(title_type)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                TitleTypeModel.__tablename__,
                title_type.uuid,
                "DELETE",
                title_type._to_dict(),
                None,
            )
        )
        db.session.commit()
        return title_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(TitleTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(TitleTypeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(TitleTypeModel).filter_by(external_id=external_id)
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
                column = getattr(TitleTypeModel, key)
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
                    db.session.query(TitleTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(TitleTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(TitleTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(TitleTypeModel).count()
        return result, total_records, page