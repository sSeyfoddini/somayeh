from app import db
from app.util.error_handlers import InternalServerError


def get_models():
    classes, models, table_names = [], [], []
    for mapper in db.Model.registry.mappers:
        try:
            models.append(mapper.class_.__name__)
            table_names.append(mapper.class_.__tablename__)
            classes.append(mapper.class_)

        except Exception as e:
            raise InternalServerError(str(e.args[0]))

    return classes, models, table_names
