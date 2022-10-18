from datetime import datetime

from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.relations_model.skills_model import SkillModel


class SkillPersistence:
    @classmethod
    def add(cls, user_id, user_name, skill):
        db.session.add(skill)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillModel.__tablename__,
                skill.id,
                "INSERT",
                None,
                skill._to_dict(),
            )
        )
        db.session.commit()
        return skill

    @classmethod
    def update(cls, user_id, user_name, skill):
        old_skill = db.session.query(SkillModel).get(skill.id)
        if old_skill is None:
            skill = SkillPersistence.add(user_id, user_name, skill)
        else:
            old_skill_clone = old_skill._clone()
            old_skill.skill_type_id = skill.skill_type_id
            old_skill.skill_name = skill.skill_name
            old_skill.skill_category_id = skill.skill_category_id
            old_skill.skill_keywords = skill.skill_keywords
            old_skill.conferring_credential = skill.conferring_credential
            old_skill.conferring_identifier = skill.conferring_identifier

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SkillModel.__tablename__,
                    skill.id,
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
                SkillModel.__tablename__,
                skill.id,
                "DELETE",
                skill._to_dict(),
                None,
            )
        )
        db.session.commit()
        return skill

    @classmethod
    def get(cls, id):
        return db.session.query(SkillModel).get(id)

    @classmethod
    def get_all(cls, page, limit):
        return SkillModel.query.limit(limit).offset((page - 1) * limit).all()
