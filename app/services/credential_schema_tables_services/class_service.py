
from app.model.credential_schema_tables_model.class_model import ClassModel
from app.persistence.credential_schema_tables_persistence.class_persistence import ClassPersistence
from app.util.error_handlers import RecordNotFound


class ClassService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        external_class_id,
        course_id,
        external_course_id,
        instructor_id,
        session_id,
        term_id,
        topic,
        reference_uri,
        delivery_id,
        location_id,
    ):

        _class = ClassModel(
            external_class_id=external_class_id,
            course_id=course_id,
            external_course_id=external_course_id,
            instructor_id=instructor_id,
            session_id=session_id,
            term_id=term_id,
            topic=topic,
            reference_uri=reference_uri,
            delivery_id=delivery_id,
            location_id=location_id
        )
        _class = ClassPersistence.add(user_id, user_name, _class)
        return _class

    @classmethod
    def update(cls,
               user_id,
               user_name,
               uuid,
               args
        ):
        _class = ClassPersistence.get(uuid)

        if _class is None:
            raise RecordNotFound("'class' with uuid '{}' not found.".format(uuid))

        _class = ClassModel(
            uuid=uuid,
            external_class_id=args.get("external_class_id", _class.external_class_id),
            course_id=args.get("course_id", _class.course_id),
            external_course_id=args.get("external_course_id", _class.external_course_id),
            instructor_id=args.get("instructor_id", _class.instructor_id),
            session_id=args.get("session_id", _class.session_id),
            term_id=args.get("term_id", _class.term_id),
            topic=args.get("topic", _class.topic),
            reference_uri=args.get("reference_uri", _class.reference_uri),
            delivery_id=args.get("delivery_id", _class.delivery_id),
            location_id=args.get("location_id", _class.location_id)
        )

        _class = ClassPersistence.update(user_id, user_name, _class)

        return _class

    @classmethod
    def delete_all(cls):
        ClassPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        _class = ClassPersistence.get(uuid)
        if _class is None:
            raise RecordNotFound("'class' with uuid '{}' not found.".format(uuid))
        ClassPersistence.delete(user_id, user_name, _class)
        return _class

    @classmethod
    def get(cls, uuid):
        _class = ClassPersistence.get(uuid)
        if _class is None:
            raise RecordNotFound("'class' with uuid '{}' not found.".format(uuid))
        return _class

    @classmethod
    def get_all(cls):
        return ClassPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return ClassPersistence.get_all_by_filter(filter_dict)
