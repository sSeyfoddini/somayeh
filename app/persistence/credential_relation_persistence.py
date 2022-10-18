from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_relation_model import CredentialRelationModel


class CredentialRelationPersistence:
    @classmethod
    def add(cls, user_id, user_name, credential_relation):
        db.session.add(credential_relation)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CredentialRelationModel.__tablename__,
                credential_relation.uuid,
                "INSERT",
                None,
                credential_relation._to_dict(),
            )
        )
        db.session.commit()
        return credential_relation

    @classmethod
    def update(cls, user_id, user_name, credential_relation):
        old_credential_relation = db.session.query(CredentialRelationModel).\
            filter_by(uuid=credential_relation.uuid).scalar()
        if old_credential_relation is None:
            credential_relation = CredentialRelationModel.add(user_id, user_name, credential_relation)
        else:
            old_credential_relation_clone = old_credential_relation._clone()
            old_credential_relation.relation_type = credential_relation.relation_type
            old_credential_relation.target_cred_type_uuid = credential_relation.target_cred_type_uuid

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CredentialRelationModel.__tablename__,
                    credential_relation.uuid,
                    "UPDATE",
                    old_credential_relation_clone._to_dict(),
                    old_credential_relation._to_dict(),
                )
            )
            db.session.commit()
            credential_relation = old_credential_relation
        return credential_relation

    @classmethod
    def delete(cls, user_id, user_name, credential_relation):
        db.session.delete(credential_relation)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CredentialRelationModel.__tablename__,
                credential_relation.uuid,
                "DELETE",
                credential_relation._to_dict(),
                None,
            )
        )
        db.session.commit()
        return credential_relation

    @classmethod
    def get(cls, uuid):
        return db.session.query(CredentialRelationModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(CredentialRelationModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(CredentialRelationModel).delete()
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
                column = getattr(CredentialRelationModel, key)
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
                    db.session.query(CredentialRelationModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(CredentialRelationModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(CredentialRelationModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(CredentialRelationModel).count()
        return result, total_records, page