import logging

from flask_restx import Namespace, Resource, cors

from app.persistence import get_models
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

field_type_ns = Namespace(
    "field_type",
    description="get fields type details",
    decorators=[cors.crossdomain(origin="*")],
)


@field_type_ns.route("/<string:cmd>")
class FieldTypeRest(Resource):
    def options(self):
        pass

    @field_type_ns.doc("return a fields type details")
    def get(self, cmd):
        try:
            classes, models, table_names = get_models()
            for model in classes:
                if cmd == model.__tablename__:
                    d = {}
                    for c in model.__table__.columns:
                        d[str(c.name)] = str(c.type)
                    return d, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
