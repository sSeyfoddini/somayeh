from sqlalchemy import asc, desc, func
from app import db
from app.model.otp_model import OtpModel


class OtpPersistence:
    @classmethod
    def add(cls, otp):
        db.session.add(otp)
        db.session.flush()
        db.session.commit()
        return otp

    @classmethod
    def update(cls, otp):
        old_otp = db.session.query(OtpModel).filter(OtpModel.email == otp.email).first()
        if old_otp is None:
            otp = OtpPersistence.add(otp)
        else:
            old_otp.email = otp.email
            old_otp.otp = otp.otp
            db.session.commit()
            otp = old_otp
        return otp

    @classmethod
    def delete(cls, otp):

        db.session.delete(otp)

        db.session.commit()
        return otp

    @classmethod
    def get(cls, uuid):
        return db.session.query(OtpModel).get(uuid)

    @classmethod
    def get_all(cls, page, limit):
        data = OtpModel.query.limit(limit).offset((page - 1) * limit).all()
        total_records = db.session.query(OtpModel).count()
        return data, total_records

    @classmethod
    def get_by_email(cls, email):
        return db.session.query(OtpModel).filter_by(email=email).first()

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
                column = getattr(OtpModel, key)
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
                    db.session.query(OtpModel)
                    .filter(*queries)
                    .order_by(desc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
            elif sort_method == "asc":
                result = (
                    db.session.query(OtpModel)
                    .filter(*queries)
                    .order_by(asc(sort_column))
                    .limit(limit)
                    .offset((page - 1) * limit)
                    .all()
                )
        else:

            result = db.session.query(OtpModel).filter(*queries).limit(limit).offset((page - 1) * limit).all()

        total_records = db.session.query(OtpModel).count()
        return result, total_records, page