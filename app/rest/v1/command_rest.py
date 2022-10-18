import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.badge_service import BadgeService
from app.services.credential_schema_tables_services.badge_type_service import BadgeTypeService
from app.services.credential_schema_tables_services.credential_type_service import CredentialTypeService
from app.services.pocket_user_credentials_services.organization_level_services import OrganizationLevelService
from app.services.pocket_user_credentials_services.organization_subtype_services import OrganizationSubtypeService
from app.services.pocket_user_credentials_services.organization_type_services import OrganizationTypeService
from app.services.skill_integrations.emsi import EmsiService
from app.services.thin_client.course_from_thin_client import Course
from app.services.thin_client.general_education_group_from_thin_client import GeneralEducationGroup
from app.services.thin_client.organization_identity_service_from_thin_client import OrgIdentity
from app.services.thin_client.program_from_thin_client import Program
from app.services.thin_client.role_from_thin_client import Role
from app.services.thin_client.term_from_thin_client import Term
from app.services.thin_client.title_from_thin_client import Title
from app.services.thin_client.learner_from_thin_client import LearnerService
from app.services.thin_client.academic_from_thin_client import Academic
from app.services.thin_client.colleges_from_thin_client import Colleges
from app.services.thin_client.class_from_thin_client import Class
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

command_ns = Namespace(
    "command",
    description="command related operations",
    decorators=[cors.crossdomain(origin="*")],
)
learner_model = command_ns.model(
    "LearnersInsertFromDataBroker", {"email_set": fields.List(fields.String(required=True))}
)

@command_ns.route("/organization")
class OrganizationRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Academic.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/skill")
class SkillRest(Resource):
    def get(self):
        try:
            EmsiService.get_skills()
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/course")
class CourseRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Course.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/organization_identity")
class OrganizationRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            OrgIdentity.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/program")
class ProgramsRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Program.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/term")
class TermRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Term.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/general_education_group")
class GeneralEducationGroupRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            GeneralEducationGroup.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/role")
class RoleRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Role.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/credential_type")
class CredentialTypeRest(Resource):
    def get(self):
        try:
            CredentialTypeService.insert()
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/organization_type")
class OrganizationTypeRest(Resource):
    def get(self):
        try:
            OrganizationTypeService.get_organization_type()
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/organization_subtype")
class OrganizationSubtypeRest(Resource):
    def get(self):
        try:
            OrganizationSubtypeService.get_organization_subtype()
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/organization_level")
class OrganizationlevelRest(Resource):
    def get(self):
        try:
            OrganizationLevelService.get_organization_level()
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/learners_insert")
class LearnersInsertRest(Resource):
    @command_ns.expect(learner_model)
    def post(self):
        args = request.get_json()

        try:
            LearnerService.insert_from_thin_client(args["email_set"])
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@command_ns.route("/learners_update")
class LearnersUpdateRest(Resource):
    @command_ns.expect(learner_model)
    def put(self):
        args = request.get_json()

        try:
            LearnerService.update_from_thin_client(args["email_set"])
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/badge_type_update_by_org_uuid/<string:uuid>")
class BadgeTypeRest(Resource):
    def options(self):
        pass

    @command_ns.doc("update from badgr")
    def get(self,uuid):
        user_id = 1
        username = "test"

        try:
            BadgeTypeService.update_from_badgr_by_org_uuid(user_id, username, uuid)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e




@command_ns.route("/title")
class TitleRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Title.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/college")
class TitleRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Colleges.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass


@command_ns.route("/badge_type_get_all_from_badgr")
class BadgeTypeRest(Resource):
    def options(self):
        pass

    def get(self):
        user_id = 1
        username = "test"
        try:
            BadgeTypeService.insert_all_from_badgr(user_id, username)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e




@command_ns.route("/badges_get_all_from_badgr")
class BadgeGetRest(Resource):
    def options(self):
        pass

    def get(self):
        try:
            BadgeService.get_all_from_badgr()
            return (
                {"message": "successful"},
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@command_ns.route("/class")
class ClassRest(Resource):
    def get(self):
        limit = request.args.get("limit", 10, type=int)

        try:
            Class.update(limit)
            return {"message": "successful"}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def options(self):
        pass
