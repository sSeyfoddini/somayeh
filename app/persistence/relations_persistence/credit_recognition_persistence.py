from datetime import datetime

from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.relations_model.credit_recognition_model import CreditRecognitionModel


class CreditRecognitionPersistence:
    @classmethod
    def add(cls, user_id, user_name, credit_recognition):
        db.session.add(credit_recognition)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CreditRecognitionModel.__tablename__,
                credit_recognition.id,
                "INSERT",
                None,
                credit_recognition._to_dict(),
            )
        )
        db.session.commit()
        return credit_recognition

    @classmethod
    def update(cls, user_id, user_name, credit_recognition):
        old_credit_recognition = db.session.query(CreditRecognitionModel).get(credit_recognition.id)
        if old_credit_recognition is None:
            credit_recognition = CreditRecognitionPersistence.add(user_id, user_name, credit_recognition)
        else:
            old_credit_recognition_clone = old_credit_recognition._clone()
            old_credit_recognition.credit_recognition_type_id = credit_recognition.credit_recognition_type_id
            old_credit_recognition.credit_recognition_name = credit_recognition.credit_recognition_name
            old_credit_recognition.credit_recognition_category_id = credit_recognition.credit_recognition_category_id
            old_credit_recognition.credit_recognition_keywords = credit_recognition.credit_recognition_keywords
            old_credit_recognition.conferring_credential = credit_recognition.conferring_credential
            old_credit_recognition.conferring_identifier = credit_recognition.conferring_identifier

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    CreditRecognitionModel.__tablename__,
                    credit_recognition.id,
                    "UPDATE",
                    old_credit_recognition_clone._to_dict(),
                    old_credit_recognition._to_dict(),
                )
            )
            db.session.commit()
            credit_recognition = old_credit_recognition
        return credit_recognition

    @classmethod
    def delete(cls, user_id, user_name, credit_recognition):
        db.session.delete(credit_recognition)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                CreditRecognitionModel.__tablename__,
                credit_recognition.id,
                "DELETE",
                credit_recognition._to_dict(),
                None,
            )
        )
        db.session.commit()
        return credit_recognition

    @classmethod
    def get(cls, id):
        return db.session.query(CreditRecognitionModel).get(id)

    @classmethod
    def get_all(cls, page, limit):
        return CreditRecognitionModel.query.limit(limit).offset((page - 1) * limit).all()
