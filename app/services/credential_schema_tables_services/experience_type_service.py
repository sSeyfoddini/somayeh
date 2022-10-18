from app.model.credential_schema_tables_model.experience_type_model import ExperienceTypeModel
from app.persistence.credential_schema_tables_persistence.experience_type_persistence import (
    ExperienceTypePersistence,
)
from app.util.error_handlers import RecordNotFound


class ExperienceTypeService:
    @classmethod
    def add(cls,
            user_id,
            user_name,
            experience_type_id,
            name,
            description,
            org_id,
            org_name,
            org_logo,
            experience_category_id,
            experience_category,
            experience_subcategory_id,
            experience_subcategory,
            image
            ):

        experience = ExperienceTypeModel(
            experience_type_id=experience_type_id,
            name=name,
            description=description,
            org_id=org_id,
            org_name=org_name,
            org_logo=org_logo,
            experience_category_id=experience_category_id,
            experience_category=experience_category,
            experience_subcategory_id=experience_subcategory_id,
            experience_subcategory=experience_subcategory,
            image=image
        )
        experience = ExperienceTypePersistence.add(user_id, user_name, experience)
        return experience

    @classmethod
    def update(cls,
               user_id,
               user_name,
               uuid,
               args
               ):
        experience = ExperienceTypePersistence.get(uuid)

        if experience is None:
            raise RecordNotFound("'experience' with uuid '{}' not found.".format(uuid))

        experience = ExperienceTypeModel(
            uuid=uuid,
            experience_type_id=args.get("experience_type_id", experience.experience_type_id),
            name=args.get("name", experience.name),
            description=args.get("description", experience.description),
            org_id=args.get("org_id", experience.org_id),
            org_name=args.get("org_name", experience.org_name),
            org_logo=args.get("org_logo", experience.org_logo),
            experience_category_id=args.get("experience_category_id", experience.experience_category_id),
            experience_category=args.get("experience_category", experience.experience_category),
            experience_subcategory_id=args.get("experience_subcategory_id", experience.experience_subcategory_id),
            experience_subcategory=args.get("experience_subcategory", experience.experience_subcategory),
            image=args.get("image", experience.image)
        )
        experience = ExperienceTypePersistence.update(user_id, user_name, experience)

        return experience

    @classmethod
    def delete_all(cls):
        ExperienceTypePersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        experience = ExperienceTypePersistence.get(uuid)
        if experience is None:
            raise RecordNotFound("'experience' with uuid '{}' not found.".format(uuid))
        ExperienceTypePersistence.delete(user_id, user_name, experience)
        return experience

    @classmethod
    def get(cls, uuid):
        experience = ExperienceTypePersistence.get(uuid)
        if experience is None:
            raise RecordNotFound("'experience' with uuid '{}' not found.".format(uuid))
        return experience

    @classmethod
    def get_all(cls):
        return ExperienceTypePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ExperienceTypePersistence.get_all_by_filter(filter_dict)

