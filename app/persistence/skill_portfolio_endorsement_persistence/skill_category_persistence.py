from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.skill_category_model import SkillCategoryModel


class SkillCategoryPersistence:
    @classmethod
    def add(cls, user_id, user_name, skill_category):
        db.session.add(skill_category)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillCategoryModel.__tablename__,
                skill_category.uuid,
                "INSERT",
                None,
                skill_category._to_dict(),
            )
        )
        db.session.commit()
        return skill_category

    @classmethod
    def update(cls, user_id, user_name, skill_category):
        old_skill_category = db.session.query(SkillCategoryModel).filter_by(uuid=skill_category.uuid).scalar()
        if old_skill_category is None:
            skill_category = SkillCategoryPersistence.add(user_id, user_name, skill_category)
        else:
            old_skill_category_clone = old_skill_category._clone()
            old_skill_category.name = skill_category.name
            old_skill_category.description = skill_category.description
            old_skill_category.reference_uri = skill_category.reference_uri

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SkillCategoryModel.__tablename__,
                    skill_category.uuid,
                    "UPDATE",
                    old_skill_category_clone._to_dict(),
                    old_skill_category._to_dict(),
                )
            )
            db.session.commit()
            skill_category = old_skill_category
        return skill_category

    @classmethod
    def delete(cls, user_id, user_name, skill_category):
        db.session.delete(skill_category)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillCategoryModel.__tablename__,
                skill_category.uuid,
                "DELETE",
                skill_category._to_dict(),
                None,
            )
        )
        db.session.commit()
        return skill_category

    @classmethod
    def get(cls, uuid):
        return db.session.query(SkillCategoryModel).filter_by(uuid=uuid).scalar()

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
                column = getattr(SkillCategoryModel, key)
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
                    db.session.query(SkillCategoryModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(SkillCategoryModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(SkillCategoryModel).filter(*queries).limit(limit).offset(
                (page - 1) * limit).all()

        total_records = db.session.query(SkillCategoryModel).count()
        return result, total_records, page