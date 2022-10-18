from datetime import datetime

from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.relations_model.coursework_model import CourseworkModel


class CourseworkPersistence:
    @classmethod
    def add(cls, user_id, user_name, coursework):
        db.session.add(coursework)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CourseworkModel.__tablename__,
                coursework.id,
                "INSERT",
                None,
                coursework._to_dict(),
            )
        )
        db.session.commit()
        return coursework

    @classmethod
    def update(cls, user_id, user_name, coursework):
        old_coursework = db.session.query(CourseworkModel).get(coursework.id)
        if old_coursework is None:
            coursework = CourseworkPersistence.add(user_id, user_name, coursework)
        else:
            old_coursework_clone = old_coursework._clone()
            old_coursework.coursework_type_id = coursework.coursework_type_id
            old_coursework.coursework_name = coursework.coursework_name
            old_coursework.coursework_category_id = coursework.coursework_category_id
            old_coursework.coursework_keywords = coursework.coursework_keywords
            old_coursework.conferring_credential = coursework.conferring_credential
            old_coursework.conferring_identifier = coursework.conferring_identifier

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CourseworkModel.__tablename__,
                    coursework.id,
                    "UPDATE",
                    old_coursework_clone._to_dict(),
                    old_coursework._to_dict(),
                )
            )
            db.session.commit()
            coursework = old_coursework
        return coursework

    @classmethod
    def delete(cls, user_id, user_name, coursework):
        db.session.delete(coursework)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CourseworkModel.__tablename__,
                coursework.id,
                "DELETE",
                coursework._to_dict(),
                None,
            )
        )
        db.session.commit()
        return coursework

    @classmethod
    def get(cls, id):
        return db.session.query(CourseworkModel).get(id)

    @classmethod
    def get_all(cls, page, limit):
        return CourseworkModel.query.limit(limit).offset((page - 1) * limit).all()
