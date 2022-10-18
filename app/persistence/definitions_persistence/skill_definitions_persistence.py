from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.definitions_model.skill_definitions_model import SkillDefinitionsModel


class SkillDefinitionsPersistence:
    @classmethod
    def add(cls, user_id, user_name, skill):
        db.session.add(skill)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillDefinitionsModel.__tablename__,
                skill.uuid,
                "INSERT",
                None,
                skill._to_dict(),
            )
        )
        db.session.commit()
        return skill

    @classmethod
    def update(cls, user_id, user_name, skill):
        old_skill = db.session.query(SkillDefinitionsModel).filter_by(uuid=skill.uuid).scalar()
        if old_skill is None:
            skill = SkillDefinitionsPersistence.add(user_id, user_name, skill)
        else:
            old_skill_clone = old_skill._clone()
            old_skill.external_id = skill.external_id
            old_skill.name = skill.name
            old_skill.description = skill.description
            old_skill.category = skill.category
            old_skill.reference_url = skill.reference_url
            old_skill.keywords = skill.keywords
            old_skill.course_code = skill.course_code
            old_skill.occupation_ids = skill.occupation_ids
            old_skill.employer_ids = skill.employer_ids

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SkillDefinitionsModel.__tablename__,
                    skill.uuid,
                    "UPDATE",
                    old_skill_clone._to_dict(),
                    old_skill._to_dict(),
                )
            )
            db.session.commit()
            skill = old_skill
        return skill

    @classmethod
    def delete(cls, user_id, user_name, skill):
        db.session.delete(skill)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillDefinitionsModel.__tablename__,
                skill.uuid,
                "DELETE",
                skill._to_dict(),
                None,
            )
        )
        db.session.commit()
        return skill

    @classmethod
    def get(cls, uuid):
        return db.session.query(SkillDefinitionsModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(SkillDefinitionsModel).all()

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
                column = getattr(SkillDefinitionsModel, key)
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
                    db.session.query(SkillDefinitionsModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(SkillDefinitionsModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(SkillDefinitionsModel).filter(*queries).limit(limit).offset(
                (page - 1) * limit).all()

        total_records = db.session.query(SkillDefinitionsModel).count()
        return result, total_records, page