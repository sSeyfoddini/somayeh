from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.organization_subtype_model import OrganizationSubtypeModel


class OrganizationSubtypePersistence:
    @classmethod
    def add(cls, user_id, user_name, organization_subtype):
        db.session.add(organization_subtype)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationSubtypeModel.__tablename__,
                organization_subtype.uuid,
                "INSERT",
                None,
                organization_subtype._to_dict(),
            )
        )

        db.session.commit()
        return organization_subtype

    @classmethod
    def update(cls, user_id, user_name, organization_subtype):
        old_organization_subtype = (
            db.session.query(OrganizationSubtypeModel).filter_by(uuid=organization_subtype.uuid).scalar()
        )

        if old_organization_subtype is None:
            organization_subtype = OrganizationSubtypePersistence.add(user_id, user_name, organization_subtype)
        else:
            old_organization_subtype_clone = old_organization_subtype._clone()
            old_organization_subtype.name = organization_subtype.name
            old_organization_subtype.description = organization_subtype.description
            old_organization_subtype.subtype_id = organization_subtype.subtype_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    OrganizationSubtypeModel.__tablename__,
                    organization_subtype.uuid,
                    "UPDATE",
                    old_organization_subtype_clone._to_dict(),
                    old_organization_subtype._to_dict(),
                )
            )
            db.session.commit()
            organization_subtype = old_organization_subtype
        return organization_subtype

    @classmethod
    def delete(cls, user_id, user_name, organization_subtype):
        db.session.delete(organization_subtype)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationSubtypeModel.__tablename__,
                organization_subtype.uuid,
                "DELETE",
                organization_subtype._to_dict(),
                None,
            )
        )
        db.session.commit()
        return organization_subtype

    @classmethod
    def get(cls, uuid):
        return db.session.query(OrganizationSubtypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(OrganizationSubtypeModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(OrganizationSubtypeModel).delete()
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
                column = getattr(OrganizationSubtypeModel, key)
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
                    db.session.query(OrganizationSubtypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(OrganizationSubtypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(OrganizationSubtypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(OrganizationSubtypeModel).count()
        return result, total_records, page