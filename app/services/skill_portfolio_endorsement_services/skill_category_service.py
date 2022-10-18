from uuid import uuid4

from app.model.skill_portfolio_endorsement_model.skill_category_model import SkillCategoryModel
from app.persistence.skill_portfolio_endorsement_persistence.skill_category_persistence import SkillCategoryPersistence
from app.util.error_handlers import RecordNotFound


class SkillCategoryService:
    @classmethod
    def add(cls, user_id, user_name, name, description, reference_uri):
        skill_category = SkillCategoryModel(name=name, description=description, reference_uri=reference_uri)
        skill_category = SkillCategoryPersistence.add(user_id, user_name, skill_category)
        return skill_category

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        skill_category = SkillCategoryPersistence.get(uuid)

        if skill_category is None:
            raise RecordNotFound("'skill category' with uuid '{}' not found.".format(uuid))

        skill_category = SkillCategoryModel(
            uuid=uuid,
            name=args.get("name", skill_category.name),
            description=args.get("description", skill_category.description),
            reference_uri=args.get("reference_uri", skill_category.reference_uri)
        )
        skill_category = SkillCategoryPersistence.update(user_id, user_name, skill_category)

        return skill_category

    @classmethod
    def delete(cls, user_id, user_name, skill_category):
        SkillCategoryPersistence.delete(user_id, user_name, skill_category)
        return skill_category

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        skill_category = SkillCategoryPersistence.get(uuid)
        if skill_category is None:
            raise RecordNotFound("'skill category' with uuid '{}' not found.".format(uuid))
        SkillCategoryPersistence.delete(user_id, user_name, skill_category)
        return skill_category

    @classmethod
    def get(cls, uuid):
        skill_category = SkillCategoryPersistence.get(uuid)
        if skill_category is None:
            raise RecordNotFound("'skill category' with uuid '{}' not found.".format(uuid))
        return skill_category

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return SkillCategoryPersistence.get_all_by_filter(filter_dict)

