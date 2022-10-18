from datetime import date


class FinalGradeModel:
    def __init__(
        self,
        recognition_date: date,
        gpa: int,
        letter_grade: str,
        program_gpa: int,
        program_letter_grade: str,
        transfer_gpa: int,
        transfer_letter_grade: str,
    ):
        self.recognition_date = recognition_date
        self.gpa = gpa
        self.letter_grade = letter_grade
        self.program_gpa = program_gpa
        self.program_letter_grade = program_letter_grade
        self.transfer_gpa = transfer_gpa
        self.transfer_letter_grade = transfer_letter_grade

    def to_dict(self):
        return {
            "recognition_date": self.recognition_date,
            "gpa": self.gpa,
            "letter_grade": self.letter_grade,
            "program_gpa": self.program_gpa,
            "program_letter_grade": self.program_letter_grade,
            "transfer_gpa": self.transfer_gpa,
            "transfer_letter_grade": self.transfer_letter_grade,
        }
