from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.general_education_model import GeneralEducationModel


class GeneralEducationPersistence:
    @classmethod
    def add(cls, user_id, user_name, general_education):
        db.session.add(general_education)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GeneralEducationModel.__tablename__,
                general_education.uuid,
                "INSERT",
                None,
                general_education._to_dict(),
            )
        )
        db.session.commit()
        return general_education

    @classmethod
    def update(cls, user_id, user_name, general_education):
        old_general_education = db.session.query(GeneralEducationModel).\
            filter_by(uuid=general_education.uuid).scalar()
        if old_general_education is None:
            general_education = GeneralEducationPersistence.add(user_id, user_name, general_education)
        else:
            old_general_education_clone = old_general_education._clone()
            old_general_education.name = general_education.name
            old_general_education.abbreviation = general_education.abbreviation
            old_general_education.description = general_education.description
            old_general_education.label = general_education.label
            old_general_education.college_id = general_education.college_id
            old_general_education.reference_uri = general_education.reference_uri
            old_general_education.type = general_education.type
            old_general_education.external_id = general_education.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    GeneralEducationModel.__tablename__,
                    general_education.uuid,
                    "UPDATE",
                    old_general_education_clone._to_dict(),
                    old_general_education._to_dict(),
                )
            )
            db.session.commit()
            general_education = old_general_education
        return general_education

    @classmethod
    def delete(cls, user_id, user_name, general_education):
        db.session.delete(general_education)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GeneralEducationModel.__tablename__,
                general_education.uuid,
                "DELETE",
                general_education._to_dict(),
                None,
            )
        )

        db.session.commit()
        return general_education

    @classmethod
    def get(cls, uuid):
        return db.session.query(GeneralEducationModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(GeneralEducationModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(GeneralEducationModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def get_all_by_filter(cls, filter_list):
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
                column = getattr(GeneralEducationModel, key)
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
                    db.session.query(GeneralEducationModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(GeneralEducationModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(GeneralEducationModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(GeneralEducationModel).count()
        return result, total_records, page