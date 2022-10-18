from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.credential_type_model import CredentialTypeModel


class CredentialTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, credential_type):
        db.session.add(credential_type)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CredentialTypeModel.__tablename__,
                credential_type.uuid,
                "INSERT",
                None,
                credential_type._to_dict(),
            )
        )

        db.session.commit()
        return credential_type

    @classmethod
    def update(cls, user_id, user_name, credential_type):
        old_credential_type = db.session.query(CredentialTypeModel).filter_by(uuid=credential_type.uuid).scalar()
        if old_credential_type is None:
            credential_type = CredentialTypePersistence.add(user_id, user_name, credential_type)
        else:
            old_credential_type_clone = old_credential_type._clone()
            old_credential_type.credential_definition_uuid = old_credential_type.credential_definition_uuid
            old_credential_type.name = credential_type.name
            old_credential_type.credential_type = credential_type.credential_type
            old_credential_type.uuid = credential_type.uuid
            old_credential_type.schema_uri = credential_type.schema_uri

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CredentialTypeModel.__tablename__,
                    credential_type.uuid,
                    "UPDATE",
                    old_credential_type_clone._to_dict(),
                    old_credential_type._to_dict(),
                )
            )
            db.session.commit()
            credential_type = old_credential_type
        return credential_type

    @classmethod
    def delete(cls, user_id, user_name, credential_type):
        db.session.delete(credential_type)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CredentialTypeModel.__tablename__,
                credential_type.uuid,
                "DELETE",
                credential_type._to_dict(),
                None,
            )
        )

        db.session.commit()
        return credential_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(CredentialTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(CredentialTypeModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(CredentialTypeModel).delete()
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
                column = getattr(CredentialTypeModel, key)
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
                    db.session.query(CredentialTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(CredentialTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(CredentialTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(CredentialTypeModel).count()
        return result, total_records, page