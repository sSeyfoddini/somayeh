from uuid import uuid4

from app.model.definitions_model.class_enrollment_definition_model import ClassEnrollmentDefinitionModel
from app.persistence.definitions_persistence.class_enrollment_definition_persistence import (
    ClassEnrollmentDefinitionPersistence,
)
from app.util.error_handlers import RecordNotFound


class ClassEnrollmentDefinitionService:
    @classmethod
    def add(cls, user_id, user_name, course_id, course_subject, course_number, course_name):

        class_enrollment_definition = ClassEnrollmentDefinitionModel(
            course_id=course_id,
            course_subject=course_subject,
            course_number=course_number,
            course_name=course_name,
        )
        class_enrollment_definition = ClassEnrollmentDefinitionPersistence.add(
            user_id, user_name, class_enrollment_definition
        )
        return class_enrollment_definition

    @classmethod
    def update(cls, user_id, user_name, uuid, args):
        class_enrollment_definition = ClassEnrollmentDefinitionPersistence.get(uuid)

        if class_enrollment_definition is None:
            raise RecordNotFound("'class enrollment definition' with uuid'{}' not found.".format(uuid))

        class_enrollment_definition = ClassEnrollmentDefinitionModel(
            uuid=uuid,
            course_id=args.get("course_id",class_enrollment_definition.course_id),
            course_subject=args.get("course_subject",class_enrollment_definition.course_subject),
            course_number=args.get("course_number",class_enrollment_definition.urse_number),
            course_name=args.get("course_name",class_enrollment_definition.course_name),
        )
        class_enrollment_definition = ClassEnrollmentDefinitionPersistence.update(
            user_id, user_name, class_enrollment_definition
        )

        return class_enrollment_definition

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        class_enrollment_definition = ClassEnrollmentDefinitionPersistence.get(uuid)
        if class_enrollment_definition is None:
            raise RecordNotFound("'class enrollment definition' with uuid'{}' not found.".format(uuid))
        ClassEnrollmentDefinitionPersistence.delete(user_id, user_name, class_enrollment_definition)
        return class_enrollment_definition

    @classmethod
    def get(cls, uuid):
        class_enrollment_definition = ClassEnrollmentDefinitionPersistence.get(uuid)
        if class_enrollment_definition is None:
            raise RecordNotFound("'class enrollment definition' with uuid'{}' not found.".format(uuid))
        return class_enrollment_definition

    @classmethod
    def get_all(cls):
        return ClassEnrollmentDefinitionPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ClassEnrollmentDefinitionPersistence.get_all_by_filter(filter_dict)
