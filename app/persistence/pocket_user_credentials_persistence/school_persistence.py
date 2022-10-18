from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.school_model import SchoolModel


class SchoolPersistence:
    @classmethod
    def add(cls, user_id, user_name, school):
        db.session.add(school)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SchoolModel.__tablename__,
                school.uuid,
                "INSERT",
                None,
                school._to_dict(),
            )
        )

        db.session.commit()
        return school

    @classmethod
    def update(cls, user_id, user_name, school):
        old_school = db.session.query(SchoolModel).filter_by(uuid=school.uuid).scalar()
        if old_school is None:
            school = SchoolPersistence.add(user_id, user_name, school)
        else:
            old_school_clone = old_school._clone()
            old_school.credential_type_id = school.credential_type_id
            old_school.school_id = school.school_id
            old_school.school_label = school.school_label
            old_school.date = school.date
            old_school.type = school.type
            old_school.external_id = school.external_id
            old_school.parent_organization = school.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SchoolModel.__tablename__,
                    school.uuid,
                    "UPDATE",
                    old_school_clone._to_dict(),
                    old_school._to_dict(),
                )
            )
            db.session.commit()
            school = old_school
        return school

    @classmethod
    def delete(cls, user_id, user_name, school):
        db.session.delete(school)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SchoolModel.__tablename__,
                school.uuid,
                "DELETE",
                school._to_dict(),
                None,
            )
        )
        db.session.commit()
        return school

    @classmethod
    def get(cls, uuid):
        return db.session.query(SchoolModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(SchoolModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(SchoolModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(SchoolModel).delete()
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
                column = getattr(SchoolModel, key)
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
                    db.session.query(SchoolModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(SchoolModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(SchoolModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(SchoolModel).count()
        return result, total_records, page