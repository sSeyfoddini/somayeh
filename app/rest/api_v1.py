import logging

from flask import Blueprint
from flask_restx import Api

from app.rest.v1.api_connection import api_connection_ns
from app.rest.v1.badg_insert_rest import badge_insert_ns
from app.rest.v1.command_rest import command_ns
from app.rest.v1.core_integration.message_rest import message_ns
from app.rest.v1.credential_schema_tables_rest.badge_rest import badge_ns
from app.rest.v1.credential_schema_tables_rest.badge_type_rest import badge_type_ns
from app.rest.v1.credential_schema_tables_rest.course_level_rest import course_level_ns
from app.rest.v1.credential_schema_tables_rest.course_rest import course_ns
from app.rest.v1.credential_schema_tables_rest.coursework_type_rest import coursework_type_ns
from app.rest.v1.credential_schema_tables_rest.credential_type_rest import credential_type_ns
from app.rest.v1.credential_schema_tables_rest.credit_recognition_type_rest import credit_recognition_type_ns
from app.rest.v1.credential_schema_tables_rest.general_education_fulfillment_rest import (
    general_education_fulfillment_ns,
)
from app.rest.v1.credential_schema_tables_rest.general_education_group_asu_rest import general_education_group_asu_ns
from app.rest.v1.credential_schema_tables_rest.general_education_rest import general_education_ns
from app.rest.v1.credential_schema_tables_rest.grade_rest import grade_ns
from app.rest.v1.credential_schema_tables_rest.instructor_rest import instructor_ns
from app.rest.v1.credential_schema_tables_rest.instructor_role_rest import instructor_role_ns
from app.rest.v1.credential_schema_tables_rest.program_completion_rest import program_completion_ns
from app.rest.v1.credential_schema_tables_rest.program_type_rest import program_type_ns
from app.rest.v1.credential_schema_tables_rest.term_rest import ns_term_ns
from app.rest.v1.credential_schema_tables_rest.experience_type_rest import experience_type_ns
from app.rest.v1.credential_schema_tables_rest.badge_partner_rest import badge_partner_ns
from app.rest.v1.definitions_rest.badge_definition_rest import badge_definition_ns
from app.rest.v1.definitions_rest.class_enrollment_definition_rest import class_enrollment_definition_ns
from app.rest.v1.fields_definition_rest import fields_definition_ns
from app.rest.v1.get_fields_rest import field_ns
from app.rest.v1.get_type_rest import field_type_ns
from app.rest.v1.health import health_database_status_ns
from app.rest.v1.model_rest import model_ns
from app.rest.v1.otp_rest import otp_ns
from app.rest.v1.pocket_user_credentials_rest.class_level_rest import class_level_ns
from app.rest.v1.pocket_user_credentials_rest.organization_identity_rest import organization_identity_ns
from app.rest.v1.pocket_user_credentials_rest.organization_level_rest import organization_level_ns
from app.rest.v1.pocket_user_credentials_rest.organization_subtype_rest import organization_subtype_ns
from app.rest.v1.pocket_user_credentials_rest.organization_type_rest import organization_type_ns
from app.rest.v1.pocket_user_credentials_rest.organizations_rest import organizations_ns
from app.rest.v1.pocket_user_credentials_rest.program_rest import program_ns
from app.rest.v1.pocket_user_credentials_rest.title_rest import title_ns
from app.rest.v1.pocket_user_credentials_rest.title_type_rest import title_type_ns
from app.rest.v1.pocket_user_credentials_rest.college_rest import college_ns
from app.rest.v1.pocket_user_credentials_rest.department_rest import department_ns
from app.rest.v1.pocket_user_credentials_rest.school_rest import school_ns
from app.rest.v1.role_rest import role_ns
from app.rest.v1.definitions_rest.skill_definitions_rest import skill_definitions_ns
from app.rest.v1.skill_portfolio_endorsement_rest.experience_category_rest import experience_category_ns
from app.rest.v1.skill_portfolio_endorsement_rest.mime_type_rest import mime_type_ns
from app.rest.v1.skill_portfolio_endorsement_rest.portfolio_source_rest import portfolio_source_ns
from app.rest.v1.skill_portfolio_endorsement_rest.skill_category_rest import skill_category_ns
from app.rest.v1.skill_portfolio_endorsement_rest.skill_type_rest import skill_type_ns
from app.rest.v1.skill_portfolio_endorsement_rest.source_skill_library_rest import source_skill_library_ns
from app.rest.v1.skill_portfolio_endorsement_rest.source_skill_type_rest import source_skill_type_ns
from app.rest.v1.thin_client.academic_from_thin_client_rest import academic_info_ns
from app.rest.v1.thin_client.colleges_from_thin_client_rest import colleges_ns
from app.rest.v1.thin_client.courses_from_thin_client_rest import courses_classes_levels_ns
from app.rest.v1.thin_client.department_from_thin_client_rest import ps_department_ns
from app.rest.v1.thin_client.employee_titles_from_thin_client_rest import ps_employee_ns
from app.rest.v1.thin_client.general_education_group_from_thin_client_rest import ps_general_ns
from app.rest.v1.thin_client.instructors_from_thin_client_rest import ps_instructor_ns
from app.rest.v1.thin_client.org_location_from_thin_client_rest import ps_org_location_ns
from app.rest.v1.thin_client.photo_from_thin_client_rest import photo_ns
from app.rest.v1.thin_client.programs_from_thin_client_rest import programs_ns
from app.rest.v1.thin_client.roles_from_thin_client_rest import ps_roles_ns
from app.rest.v1.thin_client.sa_grade_from_thin_client_rest import sa_grade_ns
from app.rest.v1.thin_client.student_from_thin_client_rest import students_ns
from app.rest.v1.thin_client.term_from_thin_client_rest import term_ns
from app.rest.v1.learners_rest import learners_ns
from app.rest.v1.credential_schema_tables_rest.class_rest import class_ns
from app.rest.v1.credential_relation_rest import credential_relation_ns
from app.rest.v1.credential_definition_rest import credential_definition_ns
from app.rest.v1.badge_object_rest import badge_object_ns

_log = logging.getLogger(__name__)

api_v1 = Blueprint("api_v1", __name__, url_prefix="/strata/v1")
api = Api(api_v1, doc="/strata/api/doc", version="1.0", title="Pocket Strata API Version 1")

api.add_namespace(class_level_ns)
api.add_namespace(college_ns)
api.add_namespace(department_ns)
api.add_namespace(school_ns)
api.add_namespace(organization_identity_ns)
api.add_namespace(organizations_ns)
api.add_namespace(organization_subtype_ns)
api.add_namespace(organization_type_ns)
api.add_namespace(program_ns)
api.add_namespace(title_ns)
api.add_namespace(title_type_ns)
api.add_namespace(model_ns)
api.add_namespace(badge_ns)
api.add_namespace(badge_type_ns)
api.add_namespace(course_level_ns)
api.add_namespace(course_ns)
api.add_namespace(coursework_type_ns)
api.add_namespace(credential_type_ns)
api.add_namespace(credit_recognition_type_ns)
api.add_namespace(general_education_fulfillment_ns)
api.add_namespace(general_education_group_asu_ns)
api.add_namespace(general_education_ns)
api.add_namespace(grade_ns)
api.add_namespace(instructor_ns)
api.add_namespace(instructor_role_ns)
api.add_namespace(program_completion_ns)
api.add_namespace(program_type_ns)
api.add_namespace(ns_term_ns)
api.add_namespace(mime_type_ns)
api.add_namespace(portfolio_source_ns)
api.add_namespace(skill_category_ns)
api.add_namespace(skill_type_ns)
api.add_namespace(source_skill_library_ns)
api.add_namespace(source_skill_type_ns)
api.add_namespace(skill_definitions_ns)
api.add_namespace(role_ns)
api.add_namespace(model_ns)
api.add_namespace(field_ns)
api.add_namespace(field_type_ns)
api.add_namespace(api_connection_ns)
api.add_namespace(badge_insert_ns)
api.add_namespace(otp_ns)
api.add_namespace(ps_org_location_ns)
api.add_namespace(academic_info_ns)
api.add_namespace(programs_ns)
api.add_namespace(colleges_ns)
api.add_namespace(term_ns)
api.add_namespace(sa_grade_ns)
api.add_namespace(students_ns)
api.add_namespace(ps_general_ns)
api.add_namespace(courses_classes_levels_ns)
api.add_namespace(health_database_status_ns)
api.add_namespace(ps_department_ns)
api.add_namespace(ps_instructor_ns)
api.add_namespace(ps_employee_ns)
api.add_namespace(ps_roles_ns)
api.add_namespace(message_ns)
api.add_namespace(learners_ns)
api.add_namespace(photo_ns)
api.add_namespace(command_ns)
api.add_namespace(fields_definition_ns)
api.add_namespace(badge_definition_ns)
api.add_namespace(class_enrollment_definition_ns)
api.add_namespace(experience_category_ns)
api.add_namespace(organization_level_ns)
api.add_namespace(class_ns)
api.add_namespace(experience_type_ns)
api.add_namespace(badge_partner_ns)
api.add_namespace(credential_relation_ns)
api.add_namespace(credential_definition_ns)
api.add_namespace(badge_object_ns)