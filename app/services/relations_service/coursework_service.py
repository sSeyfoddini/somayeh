from app.model.relations_model.coursework_model import CourseworkModel
from app.persistence.relations_persistence.coursework_persistence import CourseworkPersistence
from app.util.error_handlers import RecordNotFound

class CourseworkService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        coursework_type_id,
        coursework_name,
        coursework_category_id,
        coursework_keywords,
        conferring_credential,
        conferring_identifier,
        supporting_credential,
    ):

        coursework = CourseworkModel(
            coursework_type_id=coursework_type_id,
            coursework_name=coursework_name,
            coursework_category_id=coursework_category_id,
            coursework_keywords=coursework_keywords,
            conferring_credential=conferring_credential,
            conferring_identifier=conferring_identifier,
            supporting_credential=supporting_credential,
        )
        coursework = CourseworkPersistence.add(user_id, user_name, coursework)
        return coursework

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        id,
        args
    ):
        coursework = CourseworkPersistence.get(id)

        if coursework is None:
            raise RecordNotFound("'coursework' with id'{}' not found.".format(id))

        coursework = CourseworkModel(
            id=id,
            coursework_type_id=args.get("coursework_type_id",coursework.coursework_type_id),
            coursework_name=args.get("coursework_name",coursework.coursework_name),
            coursework_category_id=args.get("coursework_category_id",coursework.coursework_category_id),
            coursework_keywords=args.get("coursework_keywords",coursework.coursework_keywords),
            conferring_credential=args.get("conferring_credential",coursework.conferring_credential),
            conferring_identifier=args.get("conferring_identifier",coursework.conferring_identifier),
            supporting_credential=args.get("supporting_credential",coursework.supporting_credential),
        )
        coursework = CourseworkPersistence.update(user_id, user_name, coursework)

        return coursework

    @classmethod
    def delete(cls, user_id, user_name, coursework):
        CourseworkPersistence.delete(user_id, user_name, coursework)
        return coursework

    @classmethod
    def delete_by_id(cls, user_id, user_name, id):
        coursework = CourseworkPersistence.get(id)
        if coursework is None:
            raise RecordNotFound("'coursework' with id'{}' not found.".format(id))
        CourseworkPersistence.delete(user_id, user_name, coursework)
        return coursework

    @classmethod
    def get(cls, id):
        coursework = CourseworkPersistence.get(id)
        if coursework is None:
            raise RecordNotFound("'coursework' with id'{}' not found.".format(id))
        return coursework

    @classmethod
    def get_all(cls, page, limit):
        return CourseworkPersistence.get_all(page, limit)
