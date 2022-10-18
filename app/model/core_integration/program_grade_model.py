from datetime import date


class ProgramGradeModel:
    def __init__(
        self, recognition_date: date, gpa: int, letter_grade: str, program_id: str, program_name: str, term: int
    ):
        self.recognition_date = recognition_date
        self.gpa = gpa
        self.letter_grade = letter_grade
        self.program_id = program_id
        self.program_name = program_name
        self.term = term

    def to_dict(self):
        return {
            "recognition_date": self.recognition_date,
            "gpa": self.gpa,
            "letter_grade": self.letter_grade,
            "program_id": self.program_id,
            "program_name": self.program_name,
            "term": self.term,
        }
