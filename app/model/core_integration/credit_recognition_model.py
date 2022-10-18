from datetime import date


class CreditRecognitionModel:
    def __init__(
        self,
        credit_recognition_type_id: str,
        credit_recognition_type_name: str,
        source_institution_id: str,
        source_institution_name: str,
        source_credential_id: str,
        course_source_id: str,
        course_source_name: str,
        course_equivalency_id: str,
        course_equivalency_name: str,
        recognition_date: date,
        term: str,
        credit_hours: int,
        grade: str,
        general_ed: str,
        program_id: str,
        program_name: str,
    ):
        self.credit_recognition_type_id = credit_recognition_type_id
        self.credit_recognition_type_name = credit_recognition_type_name
        self.source_institution_id = source_institution_id
        self.source_institution_name = source_institution_name
        self.source_credential_id = source_credential_id
        self.course_source_id = course_source_id
        self.course_source_name = course_source_name
        self.course_equivalency_id = course_equivalency_id
        self.course_equivalency_name = course_equivalency_name
        self.recognition_date = recognition_date
        self.term = term
        self.credit_hours = credit_hours
        self.grade = grade
        self.general_ed = general_ed
        self.program_id = program_id
        self.program_name = program_name

    def to_dict(self):
        return {
            "credit_recognition_type_id": self.credit_recognition_type_id,
            "credit_recognition_type_name": self.credit_recognition_type_name,
            "source_institution_id": self.source_institution_id,
            "source_institution_name": self.source_institution_name,
            "source_credential_id": self.source_credential_id,
            "course_source_id": self.course_source_id,
            "course_source_name": self.course_source_name,
            "course_equivalency_id": self.course_equivalency_id,
            "course_equivalency_name": self.course_equivalency_name,
            "recognition_date": self.recognition_date,
            "term": self.term,
            "credit_hours": self.credit_hours,
            "grade": self.grade,
            "general_ed": self.general_ed,
            "program_id": self.program_id,
            "program_name": self.program_name,
        }
