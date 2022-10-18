from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.general_education_fulfillment_model import (
    GeneralEducationFulfillmentModel,
)


class GeneralEducationFulfillmentPersistence:
    @classmethod
    def add(cls, user_id, user_name, general_education_fulfillment):
        db.session.add(general_education_fulfillment)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GeneralEducationFulfillmentModel.__tablename__,
                general_education_fulfillment.uuid,
                "INSERT",
                None,
                general_education_fulfillment._to_dict(),
            )
        )
        db.session.commit()
        return general_education_fulfillment

    @classmethod
    def update(cls, user_id, user_name, general_education_fulfillment):
        old_general_education_fulfillment = db.session.query(GeneralEducationFulfillmentModel).\
            filter_by(uuid=general_education_fulfillment.uuid).scalar()
        if old_general_education_fulfillment is None:
            general_education_fulfillment = GeneralEducationFulfillmentPersistence.add(
                user_id, user_name, general_education_fulfillment
            )
        else:
            old_general_education_fulfillment_clone = old_general_education_fulfillment._clone()
            old_general_education_fulfillment.credential_type_id = general_education_fulfillment.credential_type_id
            old_general_education_fulfillment.credential_type_label = (
                general_education_fulfillment.credential_type_label
            )
            old_general_education_fulfillment.recognition_date = general_education_fulfillment.recognition_date
            old_general_education_fulfillment.term_id = general_education_fulfillment.term_id
            old_general_education_fulfillment.term_label = general_education_fulfillment.term_label
            old_general_education_fulfillment.gen_ed_id = general_education_fulfillment.gen_ed_id
            old_general_education_fulfillment.credential_label = general_education_fulfillment.credential_label
            old_general_education_fulfillment.gen_ed_name = general_education_fulfillment.gen_ed_name
            old_general_education_fulfillment.type = general_education_fulfillment.type
            old_general_education_fulfillment.external_id = general_education_fulfillment.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    GeneralEducationFulfillmentModel.__tablename__,
                    general_education_fulfillment.uuid,
                    "UPDATE",
                    old_general_education_fulfillment_clone._to_dict(),
                    old_general_education_fulfillment._to_dict(),
                )
            )
            db.session.commit()
            general_education_fulfillment = old_general_education_fulfillment
        return general_education_fulfillment

    @classmethod
    def delete(cls, user_id, user_name, general_education_fulfillment):
        db.session.delete(general_education_fulfillment)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GeneralEducationFulfillmentModel.__tablename__,
                general_education_fulfillment.uuid,
                "DELETE",
                general_education_fulfillment._to_dict(),
                None,
            )
        )

        db.session.commit()
        return general_education_fulfillment

    @classmethod
    def get(cls, uuid):
        return db.session.query(GeneralEducationFulfillmentModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(GeneralEducationFulfillmentModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(GeneralEducationFulfillmentModel).filter_by(external_id=external_id)
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
                column = getattr(GeneralEducationFulfillmentModel, key)
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
                    db.session.query(GeneralEducationFulfillmentModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(GeneralEducationFulfillmentModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(GeneralEducationFulfillmentModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(GeneralEducationFulfillmentModel).count()
        return result, total_records, page
