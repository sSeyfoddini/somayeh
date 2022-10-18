from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_definition_model import CredentialDefinitionModel


class CredentialDefinitionPersistence:
    @classmethod
    def add(cls, user_id, user_name, credential_definition):
        db.session.add(credential_definition)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CredentialDefinitionModel.__tablename__,
                credential_definition.uuid,
                "INSERT",
                None,
                credential_definition._to_dict(),
            )
        )
        db.session.commit()
        return credential_definition

    @classmethod
    def update(cls, user_id, user_name, credential_definition):
        old_credential_definition = db.session.query(CredentialDefinitionModel).\
            filter_by(uuid=credential_definition.uuid).scalar()
        if old_credential_definition is None:
            credential_definition = CredentialDefinitionModel.add(user_id, user_name, credential_definition)
        else:
            old_credential_definition_clone = old_credential_definition._clone()
            old_credential_definition.cred_def_type = credential_definition.cred_def_type
            old_credential_definition.cred_def = credential_definition.cred_def
            old_credential_definition.schema = credential_definition.schema
            old_credential_definition.name = credential_definition.name

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CredentialDefinitionModel.__tablename__,
                    credential_definition.uuid,
                    "UPDATE",
                    old_credential_definition_clone._to_dict(),
                    old_credential_definition._to_dict(),
                )
            )
            db.session.commit()
            credential_definition = old_credential_definition
        return credential_definition

    @classmethod
    def delete(cls, user_id, user_name, credential_definition):
        db.session.delete(credential_definition)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CredentialDefinitionModel.__tablename__,
                credential_definition.uuid,
                "DELETE",
                credential_definition._to_dict(),
                None,
            )
        )
        db.session.commit()
        return credential_definition

    @classmethod
    def get(cls, uuid):
        return db.session.query(CredentialDefinitionModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(CredentialDefinitionModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(CredentialDefinitionModel).delete()
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
                column = getattr(CredentialDefinitionModel, key)
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
                    db.session.query(CredentialDefinitionModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(CredentialDefinitionModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(CredentialDefinitionModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(CredentialDefinitionModel).count()
        return result, total_records, page