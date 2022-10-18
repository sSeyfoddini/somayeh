from datetime import datetime

from sqlalchemy import asc, desc, func

from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.badge_type_model import BadgeTypeModel


class BadgeTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, badge_type):
        db.session.add(badge_type)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgeTypeModel.__tablename__,
                badge_type.uuid,
                "INSERT",
                None,
                badge_type._to_dict(),
            )
        )
        db.session.commit()
        return badge_type

    @classmethod
    def update(cls, user_id, user_name, badge_type):
        old_badge_type = db.session.query(BadgeTypeModel).filter_by(uuid=badge_type.uuid).scalar()
        if old_badge_type is None:
            badge_type = BadgeTypePersistence.add(user_id, user_name, badge_type)
        else:
            old_badge_type_clone = old_badge_type._clone()
            old_badge_type.extrernal_partner_id = badge_type.extrernal_partner_id
            old_badge_type.extrernal_partner_label = badge_type.extrernal_partner_label
            old_badge_type.badge_org_type = badge_type.badge_org_type
            old_badge_type.badge_org_id = badge_type.badge_org_id
            old_badge_type.badge_org_label = badge_type.badge_org_label
            old_badge_type.name = badge_type.name
            old_badge_type.abbreviation = badge_type.abbreviation
            old_badge_type.description = badge_type.description
            old_badge_type.external_id = badge_type.external_id
            old_badge_type.reference_uri = badge_type.reference_uri
            old_badge_type.image = badge_type.image
            old_badge_type.attachment = badge_type.attachment
            old_badge_type.type = badge_type.type
            old_badge_type.json = badge_type.json
            old_badge_type.credential_type_uuid = badge_type.credential_type_uuid
            old_badge_type.org_uuid = badge_type.org_uuid
            old_badge_type.entityID = badge_type.entityID
            old_badge_type.auto_issue = badge_type.auto_issue

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    BadgeTypeModel.__tablename__,
                    badge_type.uuid,
                    "UPDATE",
                    old_badge_type_clone._to_dict(),
                    old_badge_type._to_dict(),
                )
            )
            db.session.commit()
            badge_type = old_badge_type
        return badge_type

    @classmethod
    def delete(cls, user_id, user_name, badge_type):
        db.session.delete(badge_type)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                BadgeTypeModel.__tablename__,
                badge_type.uuid,
                "DELETE",
                badge_type._to_dict(),
                None,
            )
        )

        db.session.commit()
        return badge_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(BadgeTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_by_entityID(cls, entityID):
        return db.session.query(BadgeTypeModel).filter_by(entityID=entityID).scalar()

    @classmethod
    def get_by_external_user_id(cls, external_id: str) -> "BadgeTypeModel":
        result = db.session.query(BadgeTypeModel).filter_by(external_id=external_id)
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
                column = getattr(BadgeTypeModel, key)
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
                    db.session.query(BadgeTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(BadgeTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:
            result = db.session.query(BadgeTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(BadgeTypeModel).count()
        return result, total_records, page

    @classmethod
    def get_all(cls):
        return db.session.query(BadgeTypeModel).all()

    @classmethod
    def get_all_uuid(cls):
        return db.session.query(BadgeTypeModel.uuid).all()