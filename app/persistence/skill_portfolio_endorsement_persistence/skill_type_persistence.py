from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.skill_type_model import SkillTypeModel


class SkillTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, skill_type):
        db.session.add(skill_type)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillTypeModel.__tablename__,
                skill_type.uuid,
                "INSERT",
                None,
                skill_type._to_dict(),
            )
        )
        db.session.commit()
        return skill_type

    @classmethod
    def update(cls, user_id, user_name, skill_type):
        old_skill_type = db.session.query(SkillTypeModel).filter_by(uuid=skill_type.uuid).scalar()
        if old_skill_type is None:
            skill_type = SkillTypePersistence.add(user_id, user_name, skill_type)
        else:
            old_skill_type_clone = old_skill_type._clone()
            old_skill_type.name = skill_type.name
            old_skill_type.description = skill_type.description
            old_skill_type.category_id = skill_type.category_id
            old_skill_type.category_name = skill_type.category_name
            old_skill_type.Updates_for_POCKMMVP_1030 = skill_type.Updates_for_POCKMMVP_1030
            old_skill_type.reference_url = skill_type.reference_url
            old_skill_type.source_skill_type_id = skill_type.source_skill_type_id
            old_skill_type.occupation_ids = skill_type.occupation_ids
            old_skill_type.employer_ids = skill_type.employer_ids
            old_skill_type.keywords = skill_type.keywords
            old_skill_type.rsd = skill_type.rsd
            old_skill_type.rsd_uri = skill_type.rsd_uri

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SkillTypeModel.__tablename__,
                    skill_type.uuid,
                    "UPDATE",
                    old_skill_type_clone._to_dict(),
                    old_skill_type._to_dict(),
                )
            )
            db.session.commit()
            skill_type = old_skill_type
        return skill_type

    @classmethod
    def delete(cls, user_id, user_name, skill_type):
        db.session.delete(skill_type)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SkillTypeModel.__tablename__,
                skill_type.uuid,
                "DELETE",
                skill_type._to_dict(),
                None,
            )
        )
        db.session.commit()
        return skill_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(SkillTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(SkillTypeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(SkillTypeModel).filter_by(external_id=external_id)
        return result.all()

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
                column = getattr(SkillTypeModel, key)
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
                    db.session.query(SkillTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(SkillTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(SkillTypeModel).filter(*queries).limit(limit).offset(
                (page - 1) * limit).all()

        total_records = db.session.query(SkillTypeModel).count()
        return result, total_records, page

    @classmethod
    def get_by_reference_url(cls, reference_url: str):
        result = db.session.query(SkillTypeModel).filter_by(reference_url=reference_url).scalar()
        return result

    @classmethod
    def delete_all(cls):
        db.session.query(SkillTypeModel).delete()
        db.session.commit()
