from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.organization_level_model import OrganizationLevelModel


class OrganizationLevelPersistence:
    @classmethod
    def add(cls, user_id, user_name, description):
        db.session.add(description)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationLevelModel.__tablename__,
                description.uuid,
                "INSERT",
                None,
                description._to_dict(),
            )
        )

        db.session.commit()
        return description

    @classmethod
    def update(cls, uuid, name, description):
        old_description = db.session.query(OrganizationLevelModel).filter_by(uuid=description.uuid).scalar()
        if old_description is None:
            description = OrganizationLevelPersistence.add(uuid, name, description)
        else:
            old_description_clone = old_description._clone()
            old_description.name = description.name
            old_description.description = description.description

            db.session.add(
                AuditLogModel.audit_log(
                    uuid,
                    name,
                    datetime.now(),
                    OrganizationLevelModel.__tablename__,
                    description.uuid,
                    "UPDATE",
                    old_description_clone._to_dict(),
                    old_description._to_dict(),
                )
            )
            db.session.commit()
            description = old_description
        return description

    @classmethod
    def delete(cls, uuid, name, description):
        db.session.delete(description)
        db.session.add(
            AuditLogModel.audit_log(
                uuid,
                name,
                datetime.now(),
                OrganizationLevelModel.__tablename__,
                description.uuid,
                "DELETE",
                description._to_dict(),
                None,
            )
        )
        db.session.commit()
        return description

    @classmethod
    def get(cls, uuid):
        return db.session.query(OrganizationLevelModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(OrganizationLevelModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(OrganizationLevelModel).delete()
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
                column = getattr(OrganizationLevelModel, key)
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
                    db.session.query(OrganizationLevelModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(OrganizationLevelModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(OrganizationLevelModel).filter(*queries).limit(limit).offset(
                (page - 1) * limit).all()

        total_records = db.session.query(OrganizationLevelModel).count()
        return result, total_records, page