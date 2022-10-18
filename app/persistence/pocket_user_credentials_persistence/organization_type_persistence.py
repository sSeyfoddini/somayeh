from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.organization_type_model import OrganizationTypeModel


class OrganizationTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, organization_type):
        db.session.add(organization_type)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationTypeModel.__tablename__,
                organization_type.uuid,
                "INSERT",
                None,
                organization_type._to_dict(),
            )
        )

        db.session.commit()
        return organization_type

    @classmethod
    def update(cls, user_id, user_name, organization_type):
        old_organization_type = db.session.query(OrganizationTypeModel).filter_by(uuid=organization_type.uuid).scalar()
        if old_organization_type is None:
            organization_type = OrganizationTypePersistence.add(user_id, user_name, organization_type)
        else:
            old_organization_type_clone = old_organization_type._clone()
            old_organization_type.name = organization_type.name
            old_organization_type.description = organization_type.description
            old_organization_type.subtype_id = organization_type.subtype_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    OrganizationTypeModel.__tablename__,
                    organization_type.uuid,
                    "UPDATE",
                    old_organization_type_clone._to_dict(),
                    old_organization_type._to_dict(),
                )
            )
            db.session.commit()
            organization_type = old_organization_type
        return organization_type

    @classmethod
    def delete(cls, user_id, user_name, organization_type):
        db.session.delete(organization_type)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationTypeModel.__tablename__,
                organization_type.uuid,
                "DELETE",
                organization_type._to_dict(),
                None,
            )
        )
        db.session.commit()
        return organization_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(OrganizationTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(OrganizationTypeModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(OrganizationTypeModel).delete()
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
                column = getattr(OrganizationTypeModel, key)
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
                    db.session.query(OrganizationTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(OrganizationTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(OrganizationTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(OrganizationTypeModel).count()
        return result, total_records, page