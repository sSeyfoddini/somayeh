from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.general_education_group_asu_model import GeneralEducationGroupASUModel


class GeneralEducationGroupASUPersistence:
    @classmethod
    def add(cls, user_id, user_name, general_education_group_asu):
        db.session.add(general_education_group_asu)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GeneralEducationGroupASUModel.__tablename__,
                general_education_group_asu.uuid,
                "INSERT",
                None,
                general_education_group_asu._to_dict(),
            )
        )
        db.session.commit()
        return general_education_group_asu

    @classmethod
    def update(cls, user_id, user_name, general_education_group_asu):
        old_general_education_group_asu = (
            db.session.query(GeneralEducationGroupASUModel).filter_by(uuid=general_education_group_asu.uuid).scalar()
        )
        if old_general_education_group_asu is None:
            general_education_group_asu = GeneralEducationGroupASUPersistence.add(
                user_id, user_name, general_education_group_asu
            )
        else:
            old_general_education_group_asu_clone = old_general_education_group_asu._clone()
            old_general_education_group_asu.name = general_education_group_asu.name
            old_general_education_group_asu.description = general_education_group_asu.description
            old_general_education_group_asu.external_id = general_education_group_asu.external_id
            old_general_education_group_asu.gen_id_list = general_education_group_asu.gen_id_list
            old_general_education_group_asu.gen_code_list = general_education_group_asu.gen_code_list
            old_general_education_group_asu.credential_type_id = general_education_group_asu.credential_type_id
            old_general_education_group_asu.parent_organization = general_education_group_asu.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    GeneralEducationGroupASUModel.__tablename__,
                    general_education_group_asu.uuid,
                    "UPDATE",
                    old_general_education_group_asu_clone._to_dict(),
                    old_general_education_group_asu._to_dict(),
                )
            )
            db.session.commit()
            general_education_group_asu = old_general_education_group_asu
        return general_education_group_asu

    @classmethod
    def delete(cls, user_id, user_name, general_education_group_asu):
        db.session.delete(general_education_group_asu)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                GeneralEducationGroupASUModel.__tablename__,
                general_education_group_asu.uuid,
                "DELETE",
                general_education_group_asu._to_dict(),
                None,
            )
        )

        db.session.commit()
        return general_education_group_asu

    @classmethod
    def get(cls, uuid):
        return db.session.query(GeneralEducationGroupASUModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(GeneralEducationGroupASUModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(GeneralEducationGroupASUModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(GeneralEducationGroupASUModel).delete()
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
                column = getattr(GeneralEducationGroupASUModel, key)
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
                    db.session.query(GeneralEducationGroupASUModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(GeneralEducationGroupASUModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(GeneralEducationGroupASUModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(GeneralEducationGroupASUModel).count()
        return result, total_records, page
