import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.badge_type_service import BadgeTypeService
from app.services.image_service import ImageService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError, InvalidImage

_log = logging.getLogger(__name__)

badge_type_ns = Namespace(
    "badge_type",
    description="BadgeType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

badge_type_add = badge_type_ns.model(
    "BadgeTypeAdd",
    {
        "extrernal_partner_id": fields.String(required=False),
        "extrernal_partner_label": fields.String(required=False),
        "badge_org_type": fields.String(required=False),
        "badge_org_id": fields.Integer(required=False),
        "badge_org_label": fields.String(required=False),
        "name": fields.String(required=True),
        "abbreviation": fields.String(required=True),
        "description": fields.String(required=True),
        "external_id": fields.String(required=True),
        "reference_uri": fields.String(required=False),
        "image": fields.String(required=False),
        "attachment": fields.String(required=False),
        "type": fields.String(required=False),
        "json": fields.String(required=False),
        "credential_type_uuid": fields.String(required=False),
        "org_uuid": fields.String(required=False),
        "entityID": fields.String(required=False),
        "auto_issue":fields.Boolean(required=True)
    },
)

badge_type_edit = badge_type_ns.model(
    "BadgeTypeEdit",
    {
        "extrernal_partner_id": fields.String(required=False),
        "extrernal_partner_label": fields.String(required=False),
        "badge_org_type": fields.String(required=False),
        "badge_org_id": fields.Integer(required=False),
        "badge_org_label": fields.String(required=False),
        "name": fields.String(required=False),
        "abbreviation": fields.String(required=False),
        "description": fields.String(required=False),
        "external_id": fields.String(required=False),
        "reference_uri": fields.String(required=False),
        "image": fields.String(required=False),
        "attachment": fields.String(required=False),
        "type": fields.String(required=False),
        "json": fields.String(required=False),
        "credential_type_uuid": fields.String(required=False),
        "org_uuid": fields.String(required=False),
        "entityID": fields.String(required=False),
        "auto_issue":fields.Boolean(required=True)
    },
)

badge_type_bulk_delete = badge_type_ns.model(
    "BadgeTypeBulkDelete", {"uuid": fields.List(fields.String(), required=True)}
)


@badge_type_ns.route("/<string:uuid>")
class BadgeTypeRest(Resource):
    def options(self):
        pass

    @badge_type_ns.doc("return a BadgeType")
    def get(self, uuid):
        try:
            badge_type = BadgeTypeService.get(uuid)
            return badge_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_type_ns.expect(badge_type_edit)
    @badge_type_ns.doc("Update a BadgeType")
    def put(self, uuid):
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        requests = dict(request.form)
        requests.update(dict(request.files))
        requests = {key: val for key, val in requests.items()}

        if requests["auto_issue"].lower() == "true":
            requests["auto_issue"] = True
        else:
            requests["auto_issue"] = False

        try:
            # todo should check the permission here
            badge_type = BadgeTypeService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=requests
            )
            return badge_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_type_ns.doc("delete a BadgeType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            badge_type = BadgeTypeService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return badge_type._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_type_ns.route("/")
class BadgeTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        try:
            if "only_uuid" in request.args:
                uuids = BadgeTypeService.get_all_uuid()
                return (
                    [uuid for uuid, in uuids],
                    200,
                    {"content-type": "application/json"},
                )
            filter_dict = request.args.to_dict()
            badge_types, total_records, page = BadgeTypeService.get_all_by_filter(filter_dict)
            if badge_types:
                return (
                    {
                        "data": [badge_type._to_dict() for badge_type in badge_types],
                        "page": {"page_number": page, "records_of_page": len(badge_types), "total_records": total_records},
                    },
                    200,
                    {"content-type": "application/json"},
                )

            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_type_ns.expect(badge_type_add)
    @badge_type_ns.doc("Create a BadgeType")
    def post(self):

        user_id = 1
        username = "test"

        # check missing field and field type
        data = {}
        requests = dict(request.form)

        if requests["auto_issue"].lower() == "true":
            requests["auto_issue"] = True
        else:
            requests["auto_issue"] = False

        for key, val in requests.items():
            try:
                data[key] = eval(val)
            except:
                data[key] = val

        try:
            CheckField.check_missing_field_and_field_type("badge_type", data)
            if "image" in request.files:
                image = request.files["image"].read()
                valid_image, image_data = ImageService.image_validation(image)
                if valid_image:
                    image_name = ImageService.upload_file(image)
                    image_data.update({"image_name": image_name})
                else:
                    raise InvalidImage("'image' is invalid image.")
            else:
                image_data = {}

            badge_type = BadgeTypeService.add(
                user_id=user_id,
                user_name=username,
                extrernal_partner_id=request.form.get("extrernal_partner_id"),
                extrernal_partner_label=request.form.get("extrernal_partner_label"),
                badge_org_type=request.form.get("badge_org_type"),
                badge_org_id=request.form.get("badge_org_id"),
                badge_org_label=request.form.get("badge_org_label"),
                name=request.form.get("name"),
                abbreviation=request.form.get("abbreviation"),
                description=request.form.get("description"),
                external_id=request.form.get("external_id"),
                reference_uri=request.form.get("reference_uri"),
                image=image_data,
                attachment=request.form.get("attachment"),
                type=request.form.get("type"),
                json=request.form.get("json"),
                credential_type_uuid=request.form.get("credential_type_uuid"),
                org_uuid=request.form.get("org_uuid"),
                entityID=request.form.get("entityID"),
                auto_issue=requests.get("auto_issue")
            )

            return badge_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):

        user_id = 1
        username = "test"
        try:
            BadgeTypeService.delete_all(user_id, username)
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_type_ns.route("/bulk_delete")
class CredentialTypeBulkDeleteRest(Resource):
    def options(self):
        pass

    @badge_type_ns.expect(badge_type_bulk_delete)
    @badge_type_ns.doc("Delete a list of Badge Type")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                BadgeTypeService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_type_ns.route("/update_from_badgr_single/<string:uuid>")
class BadgeTypeRest(Resource):
    def options(self):
        pass

    @badge_type_ns.doc("update from badgr")
    def get(self,uuid):
        user_id = 1
        username = "test"
        try:
            BadgeTypeService.update_from_badgr_single(user_id, username, uuid)
            return "Successful", 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

