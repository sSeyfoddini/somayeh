from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.experience_category_model import ExperienceCategoryModel


class ExperienceCategoryPersistence:
    @classmethod
    def add(cls, user_id, user_name, experience):
        db.session.add(experience)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ExperienceCategoryModel.__tablename__,
                experience.uuid,
                "INSERT",
                None,
                experience._to_dict(),
            )
        )
        db.session.commit()
        return experience

    @classmethod
    def update(cls, user_id, user_name, experience):
        old_experience = db.session.query(ExperienceCategoryModel).filter_by(uuid=experience.uuid).scalar()
        if old_experience is None:
            experience = cls.add(user_id, user_name, experience)
        else:
            old_experience_clone = old_experience._clone()
            old_experience.name = experience.name
            old_experience.description = experience.description
            old_experience.parent_name = experience.parent_name
            old_experience.parent_id = experience.parent_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ExperienceCategoryModel.__tablename__,
                    experience.uuid,
                    "UPDATE",
                    old_experience_clone._to_dict(),
                    old_experience._to_dict(),
                )
            )
            db.session.commit()
            experience = old_experience
        return experience

    @classmethod
    def delete(cls, user_id, user_name, experience):
        db.session.delete(experience)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ExperienceCategoryModel.__tablename__,
                experience.uuid,
                "DELETE",
                experience._to_dict(),
                None,
            )
        )
        db.session.commit()
        return experience

    @classmethod
    def get(cls, uuid):
        return db.session.query(ExperienceCategoryModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ExperienceCategoryModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(ExperienceCategoryModel).delete()
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
                column = getattr(ExperienceCategoryModel, key)
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
                    db.session.query(ExperienceCategoryModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ExperienceCategoryModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ExperienceCategoryModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ExperienceCategoryModel).count()
        return result, total_records, page
