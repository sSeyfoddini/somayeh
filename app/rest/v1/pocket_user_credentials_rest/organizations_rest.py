import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.organizations_services import OrganizationsService
from app.services.image_service import ImageService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError, InvalidImage

_log = logging.getLogger(__name__)

organizations_ns = Namespace(
    "organizations",
    description="Organizations related operations",
    decorators=[cors.crossdomain(origin="*")],
)

organizations_add = organizations_ns.model(
    "OrganizationsAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "abbreviation": fields.String(required=False),
        "type_id": fields.Integer(required=True),
        "type_name": fields.String(required=True),
        "subtype_id": fields.Integer(required=False),
        "parent_id": fields.Integer(required=False),
        "parent_name": fields.String(required=False),
        "reference_url": fields.String(required=False),
        "logo": fields.String(required=False),
        "background": fields.String(required=False),
        "mail": fields.String(required=False),
        "street_1": fields.String(requied=False),
        "street_2": fields.String(requied=False),
        "country": fields.String(requied=False),
        "city": fields.String(required=False),
        "region": fields.String(required=False),
        "postal_code": fields.String(required=False),
        "external_id": fields.String(required=False),
        "external_name": fields.String(required=False),
        "badgr_entityID": fields.String(required=False),
        "issuer_id": fields.String(required=False)
    },
)

organizations_edit = organizations_ns.model(
    "OrganizationsEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "abbreviation": fields.String(required=False),
        "type_id": fields.Integer(required=True),
        "type_name": fields.String(required=True),
        "subtype_id": fields.Integer(required=False),
        "parent_id": fields.Integer(required=False),
        "parent_name": fields.String(required=False),
        "reference_url": fields.String(required=False),
        "logo": fields.String(required=False),
        "background": fields.String(required=False),
        "mail": fields.String(required=False),
        "street_1": fields.String(requied=False),
        "street_2": fields.String(requied=False),
        "country": fields.String(requied=False),
        "city": fields.String(required=False),
        "region": fields.String(required=False),
        "postal_code": fields.String(required=False),
        "external_id": fields.String(required=False),
        "external_name": fields.String(required=False),
        "badgr_entityID": fields.String(required=False),
        "issuer_id": fields.String(required=False)
    },
)

organizations_bulk_delete = organizations_ns.model(
    "OrganizationsBulkDelete", {"uuid": fields.List(fields.String(), required=True)}
)


@organizations_ns.route("/<string:uuid>")
class OrganizationsRest(Resource):
    def options(self):
        pass

    @organizations_ns.doc("return a Organizations")
    def get(self, uuid):
        try:
            organizations = OrganizationsService.get(uuid)
            return (
                organizations._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organizations_ns.expect(organizations_edit)
    @organizations_ns.doc("Update a Organizations")
    def put(self, uuid):
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        requests = dict(request.form)
        requests.update(dict(request.files))
        requests = {key: val for key, val in requests.items()}
        try:
            # todo should check the permission here
            organizations = OrganizationsService.update(
                user_id=user_id, user_name=username, uuid=uuid, request=requests
            )
            return (
                organizations._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organizations_ns.doc("delete a Organizations")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            organizations = OrganizationsService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return (
                organizations._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organizations_ns.route("/")
class OrganizationsListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            organizationss, total_records, page = OrganizationsService.get_all_by_filter(filter_dict)
            if organizationss:
                return (
                    {
                        "data": [organizations._to_dict() for organizations in organizationss],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(organizationss),
                            "total_records": total_records,
                        },
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

    @organizations_ns.expect(organizations_add)
    @organizations_ns.doc("Create a Organizations")
    def post(self):
        user_id = 1
        username = "test"
        data = {}
        requests = dict(request.form)
        for key, val in requests.items():
            try:
                data[key] = eval(val)
            except:
                data[key] = val

        try:
            CheckField.check_missing_field_and_field_type("organizations", data)
            # check validation of images
            if "logo" in request.files:
                logo = request.files["logo"].read()
                valid_logo_image, logo_image_data = ImageService.image_validation(logo)
                if not valid_logo_image:
                    raise InvalidImage("'logo' is invalid image.")
            else:
                logo_image_data ={}
            if "background" in request.files:
                background = request.files["background"].read()
                valid_background_image, background_image_data = ImageService.image_validation(background)
                if not valid_background_image:
                    raise InvalidImage("'background' is invalid image.")
            else:
                background_image_data = {}
            # upload images
            if "logo" in request.files:
                logo_image_name = ImageService.upload_file(logo)
                logo_image_data.update({"image_name": logo_image_name})

            if "background" in request.files:
                background_image_name = ImageService.upload_file(background)
                background_image_data.update({"image_name": background_image_name})
            # add to database
            organizations = OrganizationsService.add(
                user_id=user_id,
                user_name=username,
                name=request.form.get("name"),
                description=request.form.get("description"),
                abbreviation=request.form.get("abbreviation"),
                type_id=request.form.get("type_id"),
                type_name=request.form.get("type_name"),
                subtype_id=request.form.get("subtype_id"),
                parent_id=request.form.get("parent_id"),
                parent_name=request.form.get("parent_name"),
                reference_url=request.form.get("reference_url"),
                logo=logo_image_data,
                background=background_image_data,
                mail=request.form.get("mail"),
                street_1=request.form.get("street_1"),
                street_2=request.form.get("street_2"),
                country=request.form.get("country"),
                city=request.form.get("city"),
                region=request.form.get("region"),
                postal_code=request.form.get("postal_code"),
                external_id=request.form.get("external_id"),
                external_name=request.form.get("external_name"),
                badgr_entityID=request.form.get("badgr_entityID"),
                issuer_id=request.form.get("issuer_id")
            )

            return (
                organizations._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        user_id=1
        username='test'
        try:
            OrganizationsService.delete_all(user_id=user_id, user_name=username)
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organizations_ns.route("/bulk_delete")
class OrganizationsBulkDeleteRest(Resource):
    def options(self):
        pass

    @organizations_ns.expect(organizations_bulk_delete)
    @organizations_ns.doc("Delete a list of organizations")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                OrganizationsService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e