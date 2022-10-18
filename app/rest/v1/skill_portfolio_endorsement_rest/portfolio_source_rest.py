import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.skill_portfolio_endorsement_services.portfolio_source_service import PortfolioSourceService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

portfolio_source_ns = Namespace(
    "portfolio_source",
    description="PortfolioSource related operations",
    decorators=[cors.crossdomain(origin="*")],
)

portfolio_source_add = portfolio_source_ns.model(
    "PortfolioSourceAdd",
    {
        "source_credential_id": fields.Integer(required=True),
        "source_credential_label": fields.String(required=True),
        "source_portfolio_id": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

portfolio_source_edit = portfolio_source_ns.model(
    "PortfolioSourceEdit",
    {
        "source_credential_id": fields.Integer(required=True),
        "source_credential_label": fields.String(required=True),
        "source_portfolio_id": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@portfolio_source_ns.route("/<string:uuid>")
class PortfolioSourceRest(Resource):
    def options(self):
        pass

    @portfolio_source_ns.doc("return a PortfolioSource")
    def get(self, uuid):
        try:
            portfolio_source = PortfolioSourceService.get(uuid)
            return (
                portfolio_source._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @portfolio_source_ns.expect(portfolio_source_edit)
    @portfolio_source_ns.doc("Update a PortfolioSource")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            portfolio_source = PortfolioSourceService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                portfolio_source._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @portfolio_source_ns.doc("delete a PortfolioSource")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            portfolio_source = PortfolioSourceService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return (
                portfolio_source._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@portfolio_source_ns.route("/")
class PortfolioSourceListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            portfolio_sources, total_records, page = PortfolioSourceService.get_all_by_filter(filter_dict)
            if portfolio_sources:
                return (
                    {
                        "data": [portfolio_source._to_dict() for portfolio_source in portfolio_sources],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(portfolio_sources),
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

    @portfolio_source_ns.expect(portfolio_source_add)
    @portfolio_source_ns.doc("Create a PortfolioSource")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("portfolio_source", args)
            portfolio_source = PortfolioSourceService.add(
                user_id=user_id,
                user_name=username,
                source_credential_id=args.get("source_credential_id"),
                source_credential_label=args.get("source_credential_label"),
                source_portfolio_id=args.get("source_portfolio_id"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return (
                portfolio_source._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
