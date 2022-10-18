from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.source_skill_type_model import SourceSkillTypeModel


class SourceSkillTypePersistence:
    @classmethod
    def add(cls, user_id, user_name, source_skill_type):
        db.session.add(source_skill_type)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SourceSkillTypeModel.__tablename__,
                source_skill_type.uuid,
                "INSERT",
                None,
                source_skill_type._to_dict(),
            )
        )
        db.session.commit()
        return source_skill_type

    @classmethod
    def update(cls, user_id, user_name, source_skill_type):
        old_source_skill_type = db.session.query(SourceSkillTypeModel).filter_by(uuid=source_skill_type.uuid).scalar()
        if old_source_skill_type is None:
            source_skill_type = SourceSkillTypePersistence.add(user_id, user_name, source_skill_type)
        else:
            old_source_skill_type_clone = old_source_skill_type._clone()
            old_source_skill_type.name = source_skill_type.name
            old_source_skill_type.description = source_skill_type.description
            old_source_skill_type.source_skill_library_id = source_skill_type.source_skill_library_id
            old_source_skill_type.external_id = source_skill_type.external_id
            old_source_skill_type.reference_uri = source_skill_type.reference_uri
            old_source_skill_type.category = source_skill_type.category
            old_source_skill_type.occupations = source_skill_type.occupations
            old_source_skill_type.employer = source_skill_type.employer
            old_source_skill_type.certifications = source_skill_type.certifications
            old_source_skill_type.keywords = source_skill_type.keywords
            old_source_skill_type.type = source_skill_type.type

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SourceSkillTypeModel.__tablename__,
                    source_skill_type.uuid,
                    "UPDATE",
                    old_source_skill_type_clone._to_dict(),
                    old_source_skill_type._to_dict(),
                )
            )
            db.session.commit()
            source_skill_type = old_source_skill_type
        return source_skill_type

    @classmethod
    def delete(cls, user_id, user_name, source_skill_type):
        db.session.delete(source_skill_type)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SourceSkillTypeModel.__tablename__,
                source_skill_type.uuid,
                "DELETE",
                source_skill_type._to_dict(),
                None,
            )
        )
        db.session.commit()
        return source_skill_type

    @classmethod
    def get(cls, uuid):
        return db.session.query(SourceSkillTypeModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(SourceSkillTypeModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(SourceSkillTypeModel).filter_by(external_id=external_id)
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
                column = getattr(SourceSkillTypeModel, key)
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
                    db.session.query(SourceSkillTypeModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(SourceSkillTypeModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(SourceSkillTypeModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(SourceSkillTypeModel).count()
        return result, total_records, page