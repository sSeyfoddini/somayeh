from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.college_model import CollegeModel


class CollegePersistence:
    @classmethod
    def add(cls, user_id, user_name, college):
        db.session.add(college)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CollegeModel.__tablename__,
                college.uuid,
                "INSERT",
                None,
                college._to_dict(),
            )
        )
        db.session.commit()
        return college

    @classmethod
    def update(cls, user_id, user_name, college):
        old_college = db.session.query(CollegeModel).filter_by(uuid=college.uuid).scalar()
        if old_college is None:
            college = CollegePersistence.add(user_id, user_name, college)
        else:
            old_college_clone = old_college._clone()
            old_college.credential_type_id = college.credential_type_id
            old_college.college_id = college.college_id
            old_college.college_label = college.college_label
            old_college.date = college.date
            old_college.type = college.type
            old_college.external_id = college.external_id
            old_college.parent_organization = college.parent_organization
            old_college.parent_organization = college.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CollegeModel.__tablename__,
                    college.uuid,
                    "UPDATE",
                    old_college_clone._to_dict(),
                    old_college._to_dict(),
                )
            )
            db.session.commit()
            college = old_college
        return college

    @classmethod
    def delete(cls, user_id, user_name, college):
        db.session.delete(college)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CollegeModel.__tablename__,
                college.uuid,
                "DELETE",
                college._to_dict(),
                None,
            )
        )
        db.session.commit()
        return college

    @classmethod
    def get(cls, uuid):
        return db.session.query(CollegeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(CollegeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(CollegeModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(CollegeModel).delete()
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
                column = getattr(CollegeModel, key)
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
                    db.session.query(CollegeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(CollegeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(CollegeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(CollegeModel).count()
        return result, total_records, page