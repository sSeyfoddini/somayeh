import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client_service import PhotoService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
photo_ns = Namespace(
    "photo",
    description="photo related operations",
    decorators=[cors.crossdomain(origin="*")],
)

photo_model = photo_ns.model("photo", {"EMPLID": fields.String(required=True)})


@photo_ns.route("/photo")
class Photo(Resource):
    def options(self):
        pass

    @photo_ns.expect(photo_model)
    @photo_ns.doc("fetch photo")
    def get(self):
        if request.headers.get("test") == "True":
            args = request.get_json()
            try:
                photo = PhotoService.get(args)
                if photo:
                    return photo, 200, {"content-type": "image/jpeg"}

                else:
                    return {"massage": "No content"}, 204, {"content-type": "application/json"}

            except Exception as e:

                if "status_code" not in e.__dict__:
                    e = InternalServerError(str(e.args[0]))

                _log.error(e.__dict__)

                raise e
