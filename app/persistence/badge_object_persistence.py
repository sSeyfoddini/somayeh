from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.badge_object_model import BadgeObjectModel


class BadgeObjectPersistence:
    @classmethod
    def add(cls, user_id, user_name, badge_object):
        db.session.add(badge_object)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgeObjectModel.__tablename__,
                badge_object.uuid,
                "INSERT",
                None,
                badge_object._to_dict(),
            )
        )
        db.session.commit()
        return badge_object

    @classmethod
    def update(cls, user_id, user_name, badge_object):
        old_badge_object = db.session.query(BadgeObjectModel).\
            filter_by(uuid=badge_object.uuid).scalar()
        if old_badge_object is None:
            badge_object = BadgeObjectModel.add(user_id, user_name, badge_object)
        else:
            old_badge_object_clone = old_badge_object._clone()
            old_badge_object.badge_def_uuid = badge_object.badge_def_uuid
            old_badge_object.learner_uuid = badge_object.learner_uuid
            old_badge_object.status = badge_object.status

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    BadgeObjectModel.__tablename__,
                    badge_object.uuid,
                    "UPDATE",
                    old_badge_object_clone._to_dict(),
                    old_badge_object._to_dict(),
                )
            )
            db.session.commit()
            badge_object = old_badge_object
        return badge_object

    @classmethod
    def delete(cls, user_id, user_name, badge_object):
        db.session.delete(badge_object)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgeObjectModel.__tablename__,
                badge_object.uuid,
                "DELETE",
                badge_object._to_dict(),
                None,
            )
        )
        db.session.commit()
        return badge_object

    @classmethod
    def get(cls, uuid):
        return db.session.query(BadgeObjectModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(BadgeObjectModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(BadgeObjectModel).delete()
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
                column = getattr(BadgeObjectModel, key)
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
                    db.session.query(BadgeObjectModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(BadgeObjectModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(BadgeObjectModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(BadgeObjectModel).count()
        return result, total_records, page