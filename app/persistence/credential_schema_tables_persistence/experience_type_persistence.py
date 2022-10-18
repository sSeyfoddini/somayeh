from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.credential_schema_tables_model.experience_type_model import ExperienceTypeModel


class ExperienceTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, experience):
        db.session.add(experience)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ExperienceTypeModel.__tablename__,
                experience.uuid,
                "INSERT",
                None,
                experience._to_dict(),
            )
        )
        db.session.commit()
        return experience

    @classmethod
    def update(cls, user_id, user_name, experience):
        old_experience = db.session.query(ExperienceTypeModel).filter_by(uuid=experience.uuid).scalar()
        if old_experience is None:
            experience = cls.add(user_id, user_name, experience)
        else:
            old_experience_clone = old_experience._clone()
            old_experience.experience_type_id = experience.experience_type_id
            old_experience.name = experience.name
            old_experience.description = experience.description
            old_experience.org_id = experience.org_id
            old_experience.org_name = experience.org_name
            old_experience.org_logo = experience.org_logo
            old_experience.experience_category_id = experience.experience_category_id
            old_experience.experience_category = experience.experience_category
            old_experience.experience_subcategory_id = experience.experience_subcategory_id
            old_experience.experience_subcategory = experience.experience_subcategory
            old_experience.image = experience.image

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    ExperienceTypeModel.__tablename__,
                    experience.uuid,
                    "UPDATE",
                    old_experience_clone._to_dict(),
                    old_experience._to_dict(),
                )
            )
            db.session.commit()
            experience = old_experience
        return experience

    @classmethod
    def delete(cls, user_id, user_name, experience):
        db.session.delete(experience)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                ExperienceTypeModel.__tablename__,
                experience.uuid,
                "DELETE",
                experience._to_dict(),
                None,
            )
        )
        db.session.commit()
        return experience

    @classmethod
    def get(cls, uuid):
        return db.session.query(ExperienceTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(ExperienceTypeModel).all()

    @classmethod
    def delete_all(cls):
        db.session.query(ExperienceTypeModel).delete()
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
                column = getattr(ExperienceTypeModel, key)
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
                    db.session.query(ExperienceTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(ExperienceTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(ExperienceTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(ExperienceTypeModel).count()
        return result, total_records, page
