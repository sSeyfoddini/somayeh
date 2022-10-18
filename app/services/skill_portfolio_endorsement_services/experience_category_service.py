from app.model.skill_portfolio_endorsement_model.experience_category_model import ExperienceCategoryModel
from app.persistence.skill_portfolio_endorsement_persistence.experience_category_persistence import (
    ExperienceCategoryPersistence,
)
from app.util.error_handlers import RecordNotFound


class ExperienceCategoryService:
    @classmethod
    def add(cls, user_id, user_name, name, description, parent_name, parent_id):

        experience = ExperienceCategoryModel(
            name=name, description=description, parent_name=parent_name, parent_id=parent_id
        )
        experience = ExperienceCategoryPersistence.add(user_id, user_name, experience)
        return experience

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        experience = ExperienceCategoryPersistence.get(uuid)

        if experience is None:
            raise RecordNotFound("'experience category' with uuid '{}' not found.".format(uuid))

        experience = ExperienceCategoryModel(
            uuid=uuid,
            name=args.get("name", experience.name),
            description=args.get("description", experience.description),
            parent_name=args.get("parent_name", experience.parent_name),
            parent_id=args.get("parent_id", experience.parent_id)
        )
        experience = ExperienceCategoryPersistence.update(user_id, user_name, experience)

        return experience

    @classmethod
    def delete_all(cls):
        ExperienceCategoryPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        experience = ExperienceCategoryPersistence.get(uuid)
        if experience is None:
            raise RecordNotFound("'experience category' with uuid '{}' not found.".format(uuid))
        ExperienceCategoryPersistence.delete(user_id, user_name, experience)
        return experience

    @classmethod
    def get(cls, uuid):
        experience = ExperienceCategoryPersistence.get(uuid)
        if experience is None:
            raise RecordNotFound("'experience category' with uuid '{}' not found.".format(uuid))
        return experience

    @classmethod
    def get_all(cls):
        return ExperienceCategoryPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ExperienceCategoryPersistence.get_all_by_filter(filter_dict)

