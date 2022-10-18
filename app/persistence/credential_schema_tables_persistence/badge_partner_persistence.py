from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.badge_partner_model import BadgePartnerModel


class BadgePartnerPersistence:
    @classmethod
    def add(cls, user_id, user_name, badge_partner):
        db.session.add(badge_partner)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgePartnerModel.__tablename__,
                badge_partner.uuid,
                "INSERT",
                None,
                badge_partner._to_dict(),
            )
        )

        db.session.commit()
        return badge_partner

    @classmethod
    def update(cls, user_id, user_name, badge_partner):
        old_badge_partner = db.session.query(BadgePartnerModel).filter_by(uuid=badge_partner.uuid).scalar()
        if old_badge_partner is None:
            badge_partner = BadgePartnerPersistence.add(user_id, user_name, badge_partner)
        else:
            old_badge_partner_clone = old_badge_partner._clone()
            old_badge_partner.name = badge_partner.name
            old_badge_partner.url = badge_partner.url
            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    BadgePartnerModel.__tablename__,
                    badge_partner.uuid,
                    "UPDATE",
                    old_badge_partner_clone._to_dict(),
                    old_badge_partner._to_dict(),
                )
            )
            db.session.commit()
            badge_partner = old_badge_partner
        return badge_partner

    @classmethod
    def delete(cls, user_id, user_name, badge_partner):
        db.session.delete(badge_partner)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgePartnerModel.__tablename__,
                badge_partner.uuid,
                "DELETE",
                badge_partner._to_dict(),
                None,
            )
        )
        db.session.commit()
        return badge_partner

    @classmethod
    def get(cls, uuid):
        return db.session.query(BadgePartnerModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(BadgePartnerModel).all()

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
                column = getattr(BadgePartnerModel, key)
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
                    db.session.query(BadgePartnerModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(BadgePartnerModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(BadgePartnerModel).filter(*queries).limit(limit).offset(
                (page - 1) * limit).all()

        total_records = db.session.query(BadgePartnerModel).count()
        return result, total_records, page

    @classmethod
    def delete_all(cls):
        db.session.query(BadgePartnerModel).delete()
        db.session.commit()

    @classmethod
    def get_by_url(cls, url):
        return db.session.query(BadgePartnerModel).filter_by(url=url).scalar()