import click
import logging

from app import db
from app.services.credential_schema_tables_services.badge_service import BadgeService
from app.services.credential_schema_tables_services.badge_type_service import BadgeTypeService
from app.services.credential_schema_tables_services.credential_type_service import CredentialTypeService
from app.services.skill_integrations.emsi import EmsiService
from app.services.thin_client.academic_from_thin_client import Academic
from app.services.thin_client.colleges_from_thin_client import Colleges
from app.services.thin_client.course_from_thin_client import Course
from app.services.thin_client.general_education_group_from_thin_client import GeneralEducationGroup
from app.services.thin_client.learner_from_thin_client import LearnerService
from app.services.thin_client.organization_identity_service_from_thin_client import OrgIdentity
from app.services.thin_client.program_from_thin_client import Program
from app.services.thin_client.role_from_thin_client import Role
from app.services.thin_client.term_from_thin_client import Term
from app.services.thin_client.title_from_thin_client import Title
from app.services.thin_client.class_from_thin_client import Class
from app.util.error_handlers import InternalServerError


_log = logging.getLogger(__name__)

@click.command()
@click.argument("limit", nargs=1)
def title(limit):
    try:
        Title.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
def export():
    try:
        classes = []
        for mapper in db.Model.registry.mappers:
            classes.append(mapper.class_)
        for model in classes:
            with open("tables_json/" + model.__tablename__ + ".json", "w") as file:
                file.write(str(model.__table__.columns.keys()))

        print("created json files in tables_json")

    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def organization_identity(limit):
    try:
        OrgIdentity.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def organization(limit):
    try:
        Academic.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def colleges(limit):
    try:
        Colleges.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def program(limit):
    try:
        Program.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def term(limit):
    try:
        Term.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def course(limit):
    try:
        Course.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def general(limit):
    try:
        GeneralEducationGroup.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def role(limit):
    try:
        Role.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
def credential_type():
    try:
        CredentialTypeService.insert()
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
def skill_type():
    try:
        EmsiService.get_skills()
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("email_set", nargs=1)
def learner_insert(email_set):
    try:
        email_set = email_set.strip("][").split(", ")
        LearnerService.insert_from_thin_client(email_set)

    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("email_set", nargs=1)
def learner_update(email_set):
    try:
        email_set = email_set.strip("][").split(", ")
        LearnerService.update_from_thin_client(email_set)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("uuid", nargs=1)
def badge_type_update_from_badgr_by_org_uuid(uuid):
    try:
        user_id = 1
        username = "test"
        BadgeTypeService.update_from_badgr_by_org_uuid(user_id, username, uuid)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
def badge_type_get_all_from_badgr():
    try:
        user_id = 1
        username = "test"
        BadgeTypeService.insert_all_from_badgr(user_id, username)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
def badge_get_all_from_badgr():
    try:
        BadgeService.get_all_from_badgr()
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)


@click.command()
@click.argument("limit", nargs=1)
def _class(limit):
    try:
        Class.update(limit)
    except Exception as e:
        if "status_code" not in e.__dict__:
            e = InternalServerError(str(e.args[0]))
        _log.error(e.__dict__)
        print("Error: ", e.__dict__)