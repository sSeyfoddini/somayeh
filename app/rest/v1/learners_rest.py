import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client.learner_from_thin_client import LearnerService
from app.services.learners_service import LearnersService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError, RecordNotFound

_log = logging.getLogger(__name__)

learners_ns = Namespace(
    "learners",
    description="learners related operations",
    decorators=[cors.crossdomain(origin="*")],
)

learners_add = learners_ns.model(
    "learnersAdd",
    {
        "email": fields.String(requied=True),
        "email_address_type": fields.String(requied=False),
        "address_type": fields.String(requied=False),
        "address1": fields.String(requied=False),
        "address2": fields.String(requied=False),
        "city": fields.String(requied=False),
        "county": fields.String(requied=False),
        "state": fields.String(requied=False),
        "postal_code": fields.String(requied=False),
        "effdt_addresses": fields.Date(requied=False),
        "country": fields.String(requied=False),
        "phone_type": fields.String(requied=False),
        "phone": fields.String(requied=False),
        "country_code": fields.String(requied=False),
        "pref_phone_flag": fields.String(requied=False),
        "birth_date": fields.Date(requied=False),
        "last_name": fields.String(requied=False),
        "first_name": fields.String(requied=False),
        "middle_initial": fields.String(requied=False),
        "effdt_names": fields.Date(requied=False),
        "external_id": fields.String(requied=False),
        "otp_status": fields.Boolean(requied=True),
        "user_consent": fields.Boolean(requied=False),
        "consent_date": fields.Date(requied=False),
     },
)

learners_edit = learners_ns.model(
    "learnersEdit",
    {
        "email": fields.String(requied=True),
        "email_address_type": fields.String(requied=False),
        "address_type": fields.String(requied=False),
        "address1": fields.String(requied=False),
        "address2": fields.String(requied=False),
        "city": fields.String(requied=False),
        "county": fields.String(requied=False),
        "state": fields.String(requied=False),
        "postal_code": fields.String(requied=False),
        "effdt_addresses": fields.Date(requied=False),
        "country": fields.String(requied=False),
        "phone_type": fields.String(requied=False),
        "phone": fields.String(requied=False),
        "country_code": fields.String(requied=False),
        "pref_phone_flag": fields.String(requied=False),
        "birth_date": fields.Date(requied=False),
        "last_name": fields.String(requied=False),
        "first_name": fields.String(requied=False),
        "middle_initial": fields.String(requied=False),
        "effdt_names": fields.Date(requied=False),
        "external_id": fields.String(requied=False),
        "otp_status": fields.Boolean(requied=True),
        "user_consent": fields.Boolean(requied=False),
        "consent_date": fields.Date(requied=False),
    },
)

learners_bulk_delete = learners_ns.model(
    "LearnersBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)

learner_insert_from_data_broker = learners_ns.model(
    "LearnersInsertFromDataBroker", {"email_set": fields.List(fields.String(required=True))}
)
learner_update_from_data_broker = learners_ns.model(
    "LearnersUpdateFromDataBroker", {"email_set": fields.List(fields.String(required=True))}
)
learner_consent = learners_ns.model(
    "LearnersConsent", {"Approvement": fields.Boolean(required=True),
                        "Email": fields.String(required=True)}
)

@learners_ns.route("/<string:uuid>")
class LearnersListRest(Resource):
    def options(self):
        pass

    @learners_ns.doc("Edit a learner")
    def get(self, uuid):
        try:
            learner = LearnersService.get_by_uuid(uuid)
            return learner._to_dict(), 200, {"content-type": "application/json"}
        
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @learners_ns.expect(learners_edit)
    @learners_ns.doc("Update a learner")
    def put(self, uuid):
        args = request.get_json()

        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            learner = LearnersService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return learner._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @learners_ns.doc("delete a learner")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            learner = LearnersService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return learner._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@learners_ns.route("/")
class LearnersListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            learners, total_records, page = LearnersService.get_all_by_filter(filter_dict)
            if learners:
                return (
                    {
                        "data": [learner._to_dict() for learner in learners],
                        "page": {"page_number": page, "records_of_page": len(learners),
                                 "total_records": total_records},
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

    @learners_ns.expect(learners_add)
    @learners_ns.doc("Create a learner")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("learners", args)
            
            learner = LearnersService.add(
                user_id=user_id,
                user_name=username,
                email=args.get("email"),
                email_address_type=args.get("email_address_type"),
                address_type=args.get("address_type"),
                address1=args.get("address1"),
                address2=args.get("address2"),
                city=args.get("city"),
                county=args.get("county"),
                state=args.get("state"),
                postal_code=args.get("postal_code"),
                effdt_addresses=args.get("effdt_addresses"),
                country=args.get("country"),
                phone_type=args.get("phone_type"),
                phone=args.get("phone"),
                country_code=args.get("country_code"),
                pref_phone_flag=args.get("pref_phone_flag"),
                birth_date=args.get("birth_date"),
                last_name=args.get("last_name"),
                first_name=args.get("first_name"),
                middle_initial=args.get("middle_initial"),
                effdt_names=args.get("effdt_names"),
                external_id=args.get("external_id"),
                otp_status=args.get("otp_status"),
                user_consent=args.get("user_consent"),
                consent_date=args.get("consent_date")
            )

            return learner._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            LearnersService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@learners_ns.route("/bulk_delete")
class LearnersBulkDeleteRest(Resource):
    def options(self):
        pass

    @learners_ns.expect(learners_bulk_delete)
    @learners_ns.doc("Delete a list of experience")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                LearnersService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@learners_ns.route("/insert_from_data_broker")
class LearnersInsertRest(Resource):
    def options(self):
        pass

    @learners_ns.expect(learner_insert_from_data_broker)
    @learners_ns.doc("Insert learners from data broker")
    def post(self):
        args = request.get_json()
        try:
            LearnerService.insert_from_thin_client(args["email_set"])
            return "Successful", 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@learners_ns.route("/update_from_data_broker")
class LearnersUpdateRest(Resource):
    def options(self):
        pass

    @learners_ns.expect(learner_update_from_data_broker)
    @learners_ns.doc("Update learners from data broker")
    def put(self):

        args = request.get_json()
        try:
            LearnerService.update_from_thin_client(args["email_set"])
            return "Successful", 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@learners_ns.route("/consent_status")
class LearnersConsentRest(Resource):
    def options(self):
        pass

    @learners_ns.expect(learner_consent)
    @learners_ns.doc("Update learners consent")
    def post(self):
        user_id = 1
        username = "test"
        args = request.get_json()
        try:
            learner = LearnersService.update_consent(user_id, username, args["Approvement"],args["Email"])
            return learner._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@learners_ns.route("/get_by_email/<string:email>")
class LearnersListRest(Resource):
    def options(self):
        pass

    @learners_ns.doc("Get a learner")
    def get(self, email):
        try:
            learner = LearnersService.get_by_email(email)
            if learner is None:
                raise RecordNotFound("email '{}' not found.".format(email))

            return learner._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
