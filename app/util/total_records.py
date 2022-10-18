from app import db


def get_total_records(model, queries):
    return db.session.query(model).filter(*queries).count()
