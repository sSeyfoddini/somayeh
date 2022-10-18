from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.badge_model import BadgeModel


class BadgePersistence:
    @classmethod
    def add(cls, user_id, user_name, badge):
        db.session.add(badge)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgeModel.__tablename__,
                badge.uuid,
                "INSERT",
                None,
                badge._to_dict(),
            )
        )
        db.session.commit()
        return badge

    @classmethod
    def update(cls, user_id, user_name, badge):
        old_badge = db.session.query(BadgeModel).filter_by(uuid=badge.uuid).scalar()
        if old_badge is None:
            badge = BadgePersistence.add(user_id, user_name, badge)
        else:
            old_badge_clone = old_badge._clone()
            old_badge.credential_type_id = badge.credential_type_id
            old_badge.credential_type_label = badge.credential_type_label
            old_badge.class_id = badge.class_id
            old_badge.external_user_id = badge.external_user_id
            old_badge.badge_type_uuid = badge.badge_type_uuid
            old_badge.badge_name = badge.badge_name
            old_badge.badge_description = badge.badge_description
            old_badge.badge_org_id = badge.badge_org_id
            old_badge.badge_org_label = badge.badge_org_label
            old_badge.badge_org_logo = badge.badge_org_logo
            old_badge.badge_date = badge.badge_date
            old_badge.badge_external_link = badge.badge_external_link
            old_badge.badge_image = badge.badge_image
            old_badge.badge_json = badge.badge_json
            old_badge.key = badge.key
            old_badge.learner_uuid = badge.learner_uuid

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    BadgeModel.__tablename__,
                    badge.uuid,
                    "UPDATE",
                    old_badge_clone._to_dict(),
                    old_badge._to_dict(),
                )
            )
            db.session.commit()
            badge = old_badge
        return badge

    @classmethod
    def delete(cls, user_id, user_name, badge):
        db.session.delete(badge)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgeModel.__tablename__,
                badge.uuid,
                "DELETE",
                badge._to_dict(),
                None,
            )
        )

        db.session.commit()
        return badge

    @classmethod
    def get(cls, uuid):
        return db.session.query(BadgeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(BadgeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str) -> "BadgeModel":
        result = db.session.query(BadgeModel).filter_by(external_user_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(BadgeModel).delete()
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
                column = getattr(BadgeModel, key)
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
                    db.session.query(BadgeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(BadgeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(BadgeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(BadgeModel).count()
        return result, total_records, page

    @classmethod
    def get_by_badge_external_link(cls, link):
        return db.session.query(BadgeModel).filter_by(badge_external_link=link).first()
