from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.source_skill_library_model import SourceSkillLibraryModel


class SourceSkillLibraryPersistence:
    @classmethod
    def add(cls, user_id, user_name, source_skill_library):
        db.session.add(source_skill_library)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SourceSkillLibraryModel.__tablename__,
                source_skill_library.uuid,
                "INSERT",
                None,
                source_skill_library._to_dict(),
            )
        )
        db.session.commit()
        return source_skill_library

    @classmethod
    def update(cls, user_id, user_name, source_skill_library):
        old_source_skill_library = db.session.query(SourceSkillLibraryModel).filter_by(uuid=source_skill_library.uuid).scalar()
        if old_source_skill_library is None:
            source_skill_library = SourceSkillLibraryPersistence.add(user_id, user_name, source_skill_library)
        else:
            old_source_skill_library_clone = old_source_skill_library._clone()
            old_source_skill_library.name = source_skill_library.name
            old_source_skill_library.description = source_skill_library.description
            old_source_skill_library.external_id = source_skill_library.external_id
            old_source_skill_library.reference_uri = source_skill_library.reference_uri
            old_source_skill_library.type = source_skill_library.type

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    SourceSkillLibraryModel.__tablename__,
                    source_skill_library.uuid,
                    "UPDATE",
                    old_source_skill_library_clone._to_dict(),
                    old_source_skill_library._to_dict(),
                )
            )
            db.session.commit()
            source_skill_library = old_source_skill_library
        return source_skill_library

    @classmethod
    def delete(cls, user_id, user_name, source_skill_library):
        db.session.delete(source_skill_library)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                SourceSkillLibraryModel.__tablename__,
                source_skill_library.uuid,
                "DELETE",
                source_skill_library._to_dict(),
                None,
            )
        )
        db.session.commit()
        return source_skill_library

    @classmethod
    def get(cls, uuid):
        return db.session.query(SourceSkillLibraryModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(SourceSkillLibraryModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(SourceSkillLibraryModel).filter_by(external_id=external_id)
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
                column = getattr(SourceSkillLibraryModel, key)
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
                    db.session.query(SourceSkillLibraryModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(SourceSkillLibraryModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(SourceSkillLibraryModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(SourceSkillLibraryModel).count()
        return result, total_records, page