from datetime import datetime
from sqlalchemy import asc, desc, func

from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.organization_identity_model import OrganizationIdentityModel


class OrganizationIdentityPersistence:
    @classmethod
    def add(cls, user_id, user_name, organization_identity):
        db.session.add(organization_identity)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationIdentityModel.__tablename__,
                organization_identity.uuid,
                "INSERT",
                None,
                organization_identity._to_dict(),
            )
        )

        db.session.commit()
        return organization_identity

    @classmethod
    def update(cls, user_id, user_name, organization_identity):
        old_organization_identity = (
            db.session.query(OrganizationIdentityModel).filter_by(uuid=organization_identity.uuid).scalar()
        )
        if old_organization_identity is None:
            organization_identity = OrganizationIdentityPersistence.add(user_id, user_name, organization_identity)
        else:
            old_organization_identity_clone = old_organization_identity._clone()
            old_organization_identity.credential_type_id = organization_identity.credential_type_id
            old_organization_identity.organization_label = organization_identity.organization_label
            old_organization_identity.abbreviation = organization_identity.abbreviation
            old_organization_identity.organization_type_id = organization_identity.organization_type_id
            old_organization_identity.organization_type_label = organization_identity.organization_type_label
            old_organization_identity.organization_subtype_id = organization_identity.organization_subtype_id
            old_organization_identity.organization_subtype_label = organization_identity.organization_subtype_label
            old_organization_identity.organization_parent_id = organization_identity.organization_parent_id
            old_organization_identity.organization_parent_label = organization_identity.organization_parent_label
            old_organization_identity.logo = organization_identity.logo
            old_organization_identity.background = organization_identity.background
            old_organization_identity.reference_url = organization_identity.reference_url
            old_organization_identity.street_1 = organization_identity.street_1
            old_organization_identity.street_2 = organization_identity.street_2
            old_organization_identity.country = organization_identity.country
            old_organization_identity.city = organization_identity.city
            old_organization_identity.region = organization_identity.region
            old_organization_identity.postal_code = organization_identity.postal_code
            old_organization_identity.type = organization_identity.type
            old_organization_identity.external_id = organization_identity.external_id
            old_organization_identity.parent_organization = organization_identity.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    OrganizationIdentityModel.__tablename__,
                    organization_identity.uuid,
                    "UPDATE",
                    old_organization_identity_clone._to_dict(),
                    old_organization_identity._to_dict(),
                )
            )
            db.session.commit()
            organization_identity = old_organization_identity
        return organization_identity

    @classmethod
    def delete(cls, user_id, user_name, organization_identity):
        db.session.delete(organization_identity)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                OrganizationIdentityModel.__tablename__,
                organization_identity.uuid,
                "DELETE",
                organization_identity._to_dict(),
                None,
            )
        )
        db.session.commit()
        return organization_identity

    @classmethod
    def get(cls, uuid):
        return db.session.query(OrganizationIdentityModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(OrganizationIdentityModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(OrganizationIdentityModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(OrganizationIdentityModel).delete()
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
                column = getattr(OrganizationIdentityModel, key)
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
                    db.session.query(OrganizationIdentityModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(OrganizationIdentityModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(OrganizationIdentityModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(OrganizationIdentityModel).count()
        return result, total_records, page
