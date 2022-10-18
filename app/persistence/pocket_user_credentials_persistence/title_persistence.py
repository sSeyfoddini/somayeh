from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.title_model import TitleModel


class TitlePersistence:
    @classmethod
    def add(cls, user_id, user_name, title):
        db.session.add(title)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                TitleModel.__tablename__,
                title.uuid,
                "INSERT",
                None,
                title._to_dict(),
            )
        )

        db.session.commit()
        return title

    @classmethod
    def update(cls, user_id, user_name, title):
        old_title = db.session.query(TitleModel).filter_by(uuid=title.uuid).scalar()
        if old_title is None:
            title = TitlePersistence.add(user_id, user_name, title)
        else:
            old_title_clone = old_title._clone()
            old_title.credential_type_id = title.credential_type_id
            old_title.credential_type_label = title.credential_type_label
            old_title.title_type_id = title.title_type_id
            old_title.title_type_label = title.title_type_label
            old_title.organization_id = title.organization_id
            old_title.organization_label = title.organization_label
            old_title.conferral_date = title.conferral_date
            old_title.type = title.type
            old_title.external_id = title.external_id
            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    TitleModel.__tablename__,
                    title.uuid,
                    "UPDATE",
                    old_title_clone._to_dict(),
                    old_title._to_dict(),
                )
            )
            db.session.commit()
            title = old_title
        return title

    @classmethod
    def delete(cls, user_id, user_name, title):
        db.session.delete(title)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                TitleModel.__tablename__,
                title.uuid,
                "DELETE",
                title._to_dict(),
                None,
            )
        )
        db.session.commit()
        return title

    @classmethod
    def get(cls, uuid):
        return db.session.query(TitleModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(TitleModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(TitleModel).filter_by(external_id=external_id)
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
                column = getattr(TitleModel, key)
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
                    db.session.query(TitleModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(TitleModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(TitleModel).filter(*queries).limit(limit).offset(
                (page - 1) * limit).all()

        total_records = db.session.query(TitleModel).count()
        return result, total_records, page

    @classmethod
    def delete_all(cls):
        db.session.query(TitleModel).delete()
        db.session.commit()
