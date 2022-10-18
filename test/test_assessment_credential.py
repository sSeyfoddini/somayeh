from unittest import TestCase

from app.create_app import create_app
from app.services.credential_schema_tables_services.assessment_service import AssessmentService

app = create_app()


class TryTesting(TestCase):
    def test_create_assessment(self):
        with app_context():
            assessment = AssessmentService.add(
                user_id=1,
                user_name="Test_user",
                institution_id=135453,
                external_id="external_id_test",
                name="name_test",
                abbreviation="abbreviation_test",
                description="description_test",
                reference_uri="reference_uri_test",
                type="type_test",
            )
            self.assertEqual(assessment._to_dict()["institution_id"], 135453)
            self.assertEqual(assessment._to_dict()["name"], "name_test")
            self.assertEqual(assessment._to_dict()["description"], "description_test")
            self.assertEqual(assessment._to_dict()["reference_uri"], "reference_uri_test")
            AssessmentService.delete(assessment._to_dict()["id"], "Test_user", assessment)

    def test_get_assessment(self):
        with app_context():
            assessment = AssessmentService.add(
                user_id=1,
                user_name="Test_user",
                institution_id=135453,
                external_id="external_id_test",
                name="name_test",
                abbreviation="abbreviation_test",
                description="description_test",
                reference_uri="reference_uri_test",
                type="type_test",
            )
            assessment_ = AssessmentService.get(assessment._to_dict()["id"])
            self.assertEqual(assessment_._to_dict()["institution_id"], 135453)
            self.assertEqual(assessment_._to_dict()["name"], "name_test")
            self.assertEqual(assessment_._to_dict()["description"], "description_test")
            self.assertEqual(assessment_._to_dict()["reference_uri"], "reference_uri_test")
            AssessmentService.delete(assessment._to_dict()["id"], "Test_user", assessment)

    def test_delete_assessment(self):
        with app_context():
            assessment = AssessmentService.add(
                user_id=1,
                user_name="Test_user",
                institution_id=135453,
                external_id="external_id_test",
                name="name_test",
                abbreviation="abbreviation_test",
                description="description_test",
                reference_uri="reference_uri_test",
                type="type_test",
            )
            assessment_ = AssessmentService.get(assessment._to_dict()["id"])
            AssessmentService.delete(
                assessment_._to_dict()["id"],
                assessment_._to_dict()["name"],
                assessment_,
            )
            try:
                AssessmentService.get(assessment_._to_dict()["id"])
                assert False
            except Exception:
                assert True

    def test_update_assessment(self):
        with app_context():
            assessment = AssessmentService.add(
                user_id=1,
                user_name="Test_user",
                institution_id=135453,
                external_id="external_id_test",
                name="name_test",
                abbreviation="abbreviation_test",
                description="description_test",
                reference_uri="reference_uri_test",
                type="type_test",
            )
            # update
            assessment_ = AssessmentService.update(
                user_id=3,
                user_name="Test_user_updated",
                institution_id=135453123,
                external_id="external_id_test_updated",
                name="name_test_updated",
                abbreviation="abbreviation_test_updated",
                description="description_test_updated",
                reference_uri="reference_uri_test_updated",
                type="type_test_updated",
                id=assessment._to_dict()["id"],
            )
            self.assertEqual(assessment_._to_dict()["institution_id"], 135453123)
            self.assertEqual(assessment_._to_dict()["name"], "name_test_updated")
            self.assertEqual(assessment_._to_dict()["description"], "description_test_updated")
            self.assertEqual(assessment_._to_dict()["reference_uri"], "reference_uri_test_updated")
            AssessmentService.delete(assessment_._to_dict()["id"], "Test_user_updated", assessment_)
