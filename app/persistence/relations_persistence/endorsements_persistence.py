from datetime import datetime

from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.relations_model.endorsements_model import EndorsementsModel


class EndorsementsPersistence:
    @classmethod
    def add(cls, user_id, user_name, endorsement):
        db.session.add(endorsement)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                EndorsementsModel.__tablename__,
                endorsement.id,
                "INSERT",
                None,
                endorsement._to_dict(),
            )
        )
        db.session.commit()
        return endorsement

    @classmethod
    def update(cls, user_id, user_name, endorsement):
        old_endorsement = db.session.query(EndorsementsModel).get(endorsement.id)
        if old_endorsement is None:
            endorsement = EndorsementsPersistence.add(user_id, user_name, endorsement)
        else:
            old_endorsement_clone = old_endorsement._clone()
            old_endorsement.endorsement_type_id = endorsement.endorsement_type_id
            old_endorsement.endorsement_name = endorsement.endorsement_name
            old_endorsement.endorsement_category_id = endorsement.endorsement_category_id
            old_endorsement.endorsement_keywords = endorsement.endorsement_keywords
            old_endorsement.conferring_credential = endorsement.conferring_credential
            old_endorsement.conferring_identifier = endorsement.conferring_identifier

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    EndorsementsModel.__tablename__,
                    endorsement.id,
                    "UPDATE",
                    old_endorsement_clone._to_dict(),
                    old_endorsement._to_dict(),
                )
            )
            db.session.commit()
            endorsement = old_endorsement
        return endorsement

    @classmethod
    def delete(cls, user_id, user_name, endorsement):
        db.session.delete(endorsement)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                EndorsementsModel.__tablename__,
                endorsement.id,
                "DELETE",
                endorsement._to_dict(),
                None,
            )
        )
        db.session.commit()
        return endorsement

    @classmethod
    def get(cls, id):
        return db.session.query(EndorsementsModel).get(id)

    @classmethod
    def get_all(cls, page, limit):
        return EndorsementsModel.query.limit(limit).offset((page - 1) * limit).all()
