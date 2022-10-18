from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.credit_recognition_type_model import CreditRecognitionTypeModel


class CreditRecognitionTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, credit_recognition_type):
        db.session.add(credit_recognition_type)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CreditRecognitionTypeModel.__tablename__,
                credit_recognition_type.uuid,
                "INSERT",
                None,
                credit_recognition_type._to_dict(),
            )
        )
        db.session.commit()
        return credit_recognition_type

    @classmethod
    def update(cls, user_id, user_name, credit_recognition_type):
        old_credit_recognition_type = db.session.query(CreditRecognitionTypeModel).\
            filter_by(uuid=credit_recognition_type.uuid).scalar()
        if old_credit_recognition_type is None:
            credit_recognition_type = CreditRecognitionTypePersistence.add(user_id, user_name, credit_recognition_type)
        else:
            old_credit_recognition_type_clone = old_credit_recognition_type._clone()
            old_credit_recognition_type.name = credit_recognition_type.name
            old_credit_recognition_type.description = credit_recognition_type.description
            old_credit_recognition_type.type = credit_recognition_type.type
            old_credit_recognition_type.external_id = credit_recognition_type.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CreditRecognitionTypeModel.__tablename__,
                    credit_recognition_type.uuid,
                    "UPDATE",
                    old_credit_recognition_type_clone._to_dict(),
                    old_credit_recognition_type._to_dict(),
                )
            )
            db.session.commit()
            credit_recognition_type = old_credit_recognition_type
        return credit_recognition_type

    @classmethod
    def delete(cls, user_id, user_name, credit_recognition_type):
        db.session.delete(credit_recognition_type)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CreditRecognitionTypeModel.__tablename__,
                credit_recognition_type.uuid,
                "DELETE",
                credit_recognition_type._to_dict(),
                None,
            )
        )

        db.session.commit()
        return credit_recognition_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(CreditRecognitionTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(CreditRecognitionTypeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(CreditRecognitionTypeModel).filter_by(external_id=external_id)
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
                column = getattr(CreditRecognitionTypeModel, key)
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
                    db.session.query(CreditRecognitionTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(CreditRecognitionTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(CreditRecognitionTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(CreditRecognitionTypeModel).count()
        return result, total_records, page
