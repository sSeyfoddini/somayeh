from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.pocket_user_credentials_model.department_model import DepartmentModel


class DepartmentPersistence:
    @classmethod
    def add(cls, user_id, user_name, department):
        db.session.add(department)
        db.session.flush()
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                DepartmentModel.__tablename__,
                department.uuid,
                "INSERT",
                None,
                department._to_dict(),
            )
        )
        db.session.commit()
        return department

    @classmethod
    def update(cls, user_id, user_name, department):
        old_department = db.session.query(DepartmentModel).filter_by(uuid=department.uuid).scalar()
        if old_department is None:
            department = DepartmentPersistence.add(user_id, user_name, department)
        else:
            old_department_clone = old_department._clone()
            old_department.credential_type_id = department.credential_type_id
            old_department.department_id = department.department_id
            old_department.department_label = department.department_label
            old_department.date = department.date
            old_department.type = department.type
            old_department.external_id = department.external_id
            old_department.parent_organization = department.parent_organization

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    DepartmentModel.__tablename__,
                    department.uuid,
                    "UPDATE",
                    old_department_clone._to_dict(),
                    old_department._to_dict(),
                )
            )
            db.session.commit()
            department = old_department
        return department

    @classmethod
    def delete(cls, user_id, user_name, department):
        db.session.delete(department)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                DepartmentModel.__tablename__,
                department.uuid,
                "DELETE",
                department._to_dict(),
                None,
            )
        )
        db.session.commit()
        return department

    @classmethod
    def get(cls, uuid):
        return db.session.query(DepartmentModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(DepartmentModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(DepartmentModel).filter_by(external_id=external_id)
        return result.all()

    @classmethod
    def delete_all(cls):
        db.session.query(DepartmentModel).delete()
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
                column = getattr(DepartmentModel, key)
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
                    db.session.query(DepartmentModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(DepartmentModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(DepartmentModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(DepartmentModel).count()
        return result, total_records, page