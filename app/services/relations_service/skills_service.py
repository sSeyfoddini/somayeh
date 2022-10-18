from app.model.relations_model.skills_model import SkillModel
from app.persistence.relations_persistence.skills_persistence import SkillPersistence
from app.util.error_handlers import RecordNotFound

class SkillService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        skill_type_id,
        skill_name,
        skill_category_id,
        skill_keywords,
        conferring_credential,
        conferring_identifier,
        supporting_credential,
    ):

        skill = SkillModel(
            skill_type_id=skill_type_id,
            skill_name=skill_name,
            skill_category_id=skill_category_id,
            skill_keywords=skill_keywords,
            conferring_credential=conferring_credential,
            conferring_identifier=conferring_identifier,
            supporting_credential=supporting_credential,
        )
        skill = SkillPersistence.add(user_id, user_name, skill)
        return skill

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        id,
        args
    ):
        skill = SkillPersistence.get(id)

        if skill is None:
            raise RecordNotFound("'skill' with uuid'{}' not found.".format(uuid))

        skill = SkillModel(
            id=id,
            skill_type_id=args.get("skill_type_id", skill.skill_type_id),
            skill_name=args.get("skill_name", skill.skill_name),
            skill_category_id=args.get("skill_category_id", skill.skill_category_id),
            skill_keywords=args.get("skill_keywords", skill.skill_keywords),
            conferring_credential=args.get("conferring_credential", skill.conferring_credential),
            conferring_identifier=args.get("conferring_identifier", skill.onferring_identifier),
            supporting_credential=args.get("supporting_credential", skill.supporting_credential),
        )
        skill = SkillPersistence.update(user_id, user_name, skill)

        return skill

    @classmethod
    def delete(cls, user_id, user_name, skill):
        SkillPersistence.delete(user_id, user_name, skill)
        return skill

    @classmethod
    def delete_by_id(cls, user_id, user_name, id):
        skill = SkillPersistence.get(id)
        if skill is None:
            raise RecordNotFound("'skill' with uuid'{}' not found.".format(uuid))
        SkillPersistence.delete(user_id, user_name, skill)
        return skill

    @classmethod
    def get(cls, id):
        skill = SkillPersistence.get(id)
        if skill is None:
            raise RecordNotFound("'skill' with uuid'{}' not found.".format(uuid))
        return skill

    @classmethod
    def get_all(cls, page, limit):
        return SkillPersistence.get_all(page, limit)
