from datetime import date


class TermGradeModel:
    def __init__(self, recognition_date: date, gpa: int, letter_grade: str, term: str):
        self.recognition_date = recognition_date
        self.gpa = gpa
        self.letter_grade = letter_grade
        self.term = term

    def to_dict(self):
        return {
            "recognition_date": self.recognition_date,
            "gpa": self.gpa,
            "letter_grade": self.letter_grade,
            "term": self.term,
        }
