from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.learners_model import LearnersModel


class LearnersPersistence:
    @classmethod
    def add(cls, user_id, user_name, learner):
        db.session.add(learner)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                LearnersModel.__tablename__,
                learner.uuid,
                "INSERT",
                None,
                learner._to_dict(),
            )
        )
        db.session.commit()
        return learner

    @classmethod
    def update(cls, user_id, user_name, learner):
        old_learner = db.session.query(LearnersModel).filter_by(uuid=learner.uuid).scalar()
        if old_learner is None:
            learner = cls.add(user_id, user_name, learner)
        else:
            old_learner_clone = old_learner._clone()
            old_learner.email = learner.email
            old_learner.email_address_type = learner.email_address_type
            old_learner.address_type = learner.address_type
            old_learner.address1 = learner.address1
            old_learner.address2 = learner.address2
            old_learner.city = learner.city
            old_learner.county = learner.county
            old_learner.state = learner.state
            old_learner.postal_code = learner.postal_code
            old_learner.effdt_addresses = learner.effdt_addresses
            old_learner.country = learner.country
            old_learner.phone_type = learner.phone_type
            old_learner.phone = learner.phone
            old_learner.country_code = learner.country_code
            old_learner.pref_phone_flag = learner.pref_phone_flag
            old_learner.birth_date = learner.birth_date
            old_learner.last_name = learner.last_name
            old_learner.first_name = learner.first_name
            old_learner.middle_initial = learner.middle_initial
            old_learner.effdt_names = learner.effdt_names
            old_learner.external_id = learner.external_id
            old_learner.otp_status = learner.otp_status
            old_learner.uuid = learner.uuid
            old_learner.user_consent = learner.user_consent
            old_learner.consent_date = learner.consent_date

            # db.session.add(
            #     AuditLogModel.audit_log(
            #         user_id,
            #         user_name,
            #         datetime.now(),
            #         LearnersModel.__tablename__,
            #         learner.uuid,
            #         "UPDATE",
            #         old_learner_clone._to_dict(),
            #         old_learner._to_dict(),
            #     )
            # )
            db.session.commit()
            learner = old_learner
        return learner

    @classmethod
    def delete(cls, user_id, user_name, learner):
        db.session.delete(learner)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                LearnersModel.__tablename__,
                learner.uuid,
                "DELETE",
                learner._to_dict(),
                None,
            )
        )
        db.session.commit()
        return learner

    @classmethod
    def get_by_email(cls, email):
        return db.session.query(LearnersModel).filter_by(email=email).scalar()

    @classmethod
    def get_by_uuid(cls, uuid):
        return db.session.query(LearnersModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(LearnersModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(LearnersModel).delete()
        db.session.commit()
    
    @classmethod
    def get_all_by_filter(
            cls,
            filter_list
    ):
        page = 1
        limit = 10
        sort = None
        queries = []
        for key, val in filter_list.items():
            if key == "page":
                page = int(val)
            elif key == "limit":
                limit = int(val)
            elif key == "sort":
                sort = val
            else:
                column = getattr(LearnersModel, key)
                if key == "uuid":
                    queries.append(func.lower(column) == func.lower(val))
                elif column.type.python_type == str:
                    queries.append(func.lower(column).contains(func.lower(val)))
                elif column.type.python_type == int or column.type.python_type == float \
                    or column.type.python_type == bool or column.type.python_type == datetime:
                    queries.append(column == val)
                else:
                    queries.append(column.contains(val))

        if sort:
            sort_column, sort_method = sort.split(":", 1)
            if sort_method == "desc":
                result = (
                    db.session.query(LearnersModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(LearnersModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(LearnersModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(LearnersModel).count()
        return result, total_records, page