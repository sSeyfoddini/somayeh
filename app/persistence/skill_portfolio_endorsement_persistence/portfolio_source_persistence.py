from datetime import datetime
from sqlalchemy import asc, desc, func
from app import db
from app.model.audit_log_model import AuditLogModel
from app.model.skill_portfolio_endorsement_model.portfolio_source_model import PortfolioSourceModel


class PortfolioSourcePersistence:
    @classmethod
    def add(cls, user_id, user_name, portfolio_source):
        db.session.add(portfolio_source)
        db.session.flush()

        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                PortfolioSourceModel.__tablename__,
                portfolio_source.uuid,
                "INSERT",
                None,
                portfolio_source._to_dict(),
            )
        )
        db.session.commit()
        return portfolio_source

    @classmethod
    def update(cls, user_id, user_name, portfolio_source):
        old_portfolio_source = db.session.query(PortfolioSourceModel).filter_by(uuid=portfolio_source.uuid).scalar()
        if old_portfolio_source is None:
            portfolio_source = PortfolioSourcePersistence.add(user_id, user_name, portfolio_source)
        else:
            old_portfolio_source_clone = old_portfolio_source._clone()
            old_portfolio_source.source_credential_id = portfolio_source.source_credential_id
            old_portfolio_source.source_credential_label = portfolio_source.source_credential_label
            old_portfolio_source.source_portfolio_id = portfolio_source.source_portfolio_id
            old_portfolio_source.type = portfolio_source.type
            old_portfolio_source.external_id = portfolio_source.external_id

            db.session.add(
                AuditLogModel.audit_log(
                    user_id,
                    user_name,
                    datetime.now(),
                    PortfolioSourceModel.__tablename__,
                    portfolio_source.uuid,
                    "UPDATE",
                    old_portfolio_source_clone._to_dict(),
                    old_portfolio_source._to_dict(),
                )
            )
            db.session.commit()
            portfolio_source = old_portfolio_source
        return portfolio_source

    @classmethod
    def delete(cls, user_id, user_name, portfolio_source):
        db.session.delete(portfolio_source)
        db.session.add(
            AuditLogModel.audit_log(
                user_id,
                user_name,
                datetime.now(),
                PortfolioSourceModel.__tablename__,
                portfolio_source.uuid,
                "DELETE",
                portfolio_source._to_dict(),
                None,
            )
        )
        db.session.commit()
        return portfolio_source

    @classmethod
    def get(cls, uuid):
        return db.session.query(PortfolioSourceModel).filter_by(uuid=uuid).scalar()

    @classmethod
    def get_all(cls):
        return db.session.query(PortfolioSourceModel).all()

    @classmethod
    def get_by_external_user_id(cls, external_id: str):
        result = db.session.query(PortfolioSourceModel).filter_by(external_id=external_id)
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
                column = getattr(PortfolioSourceModel, key)
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
                    db.session.query(PortfolioSourceModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(PortfolioSourceModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(PortfolioSourceModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(PortfolioSourceModel).count()
        return result, total_records, page
