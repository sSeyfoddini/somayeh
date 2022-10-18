from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.organizations_model import OrganizationsModel
from app.util.total_records import get_total_records


class OrganizationsPersistence:
    @classmethod
    def add(cls, user_id, user_name, organizations):
        db.session.add(organizations)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationsModel.__tablename__,
                organizations.uuid,
                "INSERT",
                None,
                organizations._to_dict(),
            )
        )

        db.session.commit()
        return organizations

    @classmethod
    def update(cls, user_id, user_name, organizations):
        old_organizations = db.session.query(OrganizationsModel).filter_by(uuid=organizations.uuid).scalar()
        if old_organizations is None:
            organizations = OrganizationsPersistence.add(user_id, user_name, organizations)
        else:
            old_organizations_clone = old_organizations._clone()
            old_organizations.name = organizations.name
            old_organizations.description = organizations.description
            old_organizations.abbreviation = organizations.abbreviation
            old_organizations.type_id = organizations.type_id
            old_organizations.type_name = organizations.type_name
            old_organizations.subtype_id = organizations.subtype_id
            old_organizations.parent_id = organizations.parent_id
            old_organizations.parent_name = organizations.parent_name
            old_organizations.reference_url = organizations.reference_url
            old_organizations.logo = organizations.logo
            old_organizations.background = organizations.background
            old_organizations.mail = organizations.mail
            old_organizations.street_1 = organizations.street_1
            old_organizations.street_2 = organizations.street_2
            old_organizations.country = organizations.country
            old_organizations.city = organizations.city
            old_organizations.region = organizations.region
            old_organizations.postal_code = organizations.postal_code
            old_organizations.external_id = organizations.external_id
            old_organizations.external_name = organizations.external_name
            old_organizations.badgr_entityID = organizations.badgr_entityID
            old_organizations.issuer_id = organizations.issuer_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    OrganizationsModel.__tablename__,
                    organizations.uuid,
                    "UPDATE",
                    old_organizations_clone._to_dict(),
                    old_organizations._to_dict(),
                )
            )
            db.session.commit()
            organizations = old_organizations
        return organizations

    @classmethod
    def delete(cls, user_id, user_name, organizations):
        db.session.delete(organizations)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationsModel.__tablename__,
                organizations.uuid,
                "DELETE",
                organizations._to_dict(),
                None,
            )
        )
        db.session.commit()
        return organizations

    @classmethod
    def get(cls, uuid):
        return db.session.query(OrganizationsModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(OrganizationsModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(OrganizationsModel).delete()
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
                column = getattr(OrganizationsModel, key)
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
                    db.session.query(OrganizationsModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(OrganizationsModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(OrganizationsModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = get_total_records(OrganizationsModel, queries)
        return result, total_records, page

    @classmethod
    def get_by_badgr_entityId(cls,badgr_entityId):
        return db.session.query(OrganizationsModel).filter_by(badgr_entityID=badgr_entityId).scalar()