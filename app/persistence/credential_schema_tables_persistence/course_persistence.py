from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.course_model import CourseModel


class CoursePersistence:
    @classmethod
    def add(cls, user_id, user_name, course):
        db.session.add(course)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CourseModel.__tablename__,
                course.uuid,
                "INSERT",
                None,
                course._to_dict(),
            )
        )
        db.session.commit()
        return course

    @classmethod
    def update(cls, user_id, user_name, course):
        old_course = db.session.query(CourseModel).filter_by(uuid=course.uuid).scalar()
        if old_course is None:
            course = CoursePersistence.add(user_id, user_name, course)
        else:
            old_course_clone = old_course._clone()
            old_course.external_id = course.external_id
            old_course.subject_code = course.subject_code
            old_course.catalog_code = course.catalog_code
            old_course.reference_uri = course.reference_uri
            old_course.college_id = course.college_id
            old_course.school_id = course.school_id
            old_course.name = course.name
            old_course.description = course.description
            old_course.credit_hours = course.credit_hours
            old_course.course_level_id = course.course_level_id
            old_course.general_ed_id_required = course.general_ed_id_required
            old_course.general_ed_id_credit = course.general_ed_id_credit
            old_course.program_id_required = course.program_id_required
            old_course.program_id_credit = course.program_id_credit
            old_course.type = course.type
            old_course.credential_type_id = course.credential_type_id
            old_course.parent_organization = course.parent_organization
            old_course.uuid = course.uuid
            old_course.key = course.key

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CourseModel.__tablename__,
                    course.uuid,
                    "UPDATE",
                    old_course_clone._to_dict(),
                    old_course._to_dict(),
                )
            )
            db.session.commit()
            course = old_course
        return course

    @classmethod
    def delete(cls, user_id, user_name, course):
        db.session.delete(course)

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CourseModel.__tablename__,
                course.uuid,
                "DELETE",
                course._to_dict(),
                None,
            )
        )

        db.session.commit()
        return course

    @classmethod
    def get(cls, uuid):
        return db.session.query(CourseModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls, page, limit):
        data = CourseModel.query.limit(limit).offset((page - 1) * limit).all()
        total_records = db.session.query(CourseModel).count()
        return data, total_records

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(CourseModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(CourseModel).delete()
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
                column = getattr(CourseModel, key)
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
                    db.session.query(CourseModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(CourseModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:
            result = db.session.query(CourseModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(CourseModel).count()
        return result, total_records, page