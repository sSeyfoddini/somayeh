from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.skill_keyword_model import SkillKeywordModel


class SkillKeywordPersistence:
    @classmethod
    def add(cls, user_id, user_name, skill_keyword):
        db.session.add(skill_keyword)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillKeywordModel.__tablename__,
                skill_keyword.uuid,
                "INSERT",
                None,
                skill_keyword._to_dict(),
            )
        )
        db.session.commit()
        return skill_keyword

    @classmethod
    def update(cls, user_id, user_name, skill_keyword):
        old_skill_keyword = db.session.query(SkillKeywordModel).filter_by(uuid=skill_keyword.uuid).scalar()
        if old_skill_keyword is None:
            skill_keyword = SkillKeywordPersistence.add(user_id, user_name, skill_keyword)
        else:
            old_skill_keyword_clone = old_skill_keyword._clone()
            old_skill_keyword.keyword = skill_keyword.keyword

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SkillKeywordModel.__tablename__,
                    skill_keyword.uuid,
                    "UPDATE",
                    old_skill_keyword_clone._to_dict(),
                    old_skill_keyword._to_dict(),
                )
            )
            db.session.commit()
            skill_keyword = old_skill_keyword
        return skill_keyword

    @classmethod
    def delete(cls, user_id, user_name, skill_keyword):
        db.session.delete(skill_keyword)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillKeywordModel.__tablename__,
                skill_keyword.uuid,
                "DELETE",
                skill_keyword._to_dict(),
                None,
            )
        )
        db.session.commit()
        return skill_keyword

    @classmethod
    def get(cls, uuid):
        return db.session.query(SkillKeywordModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(SkillKeywordModel).all()

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
                column = getattr(SkillKeywordModel, key)
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
                    db.session.query(SkillKeywordModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(SkillKeywordModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(SkillKeywordModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(SkillKeywordModel).count()
        return result, total_records, page
