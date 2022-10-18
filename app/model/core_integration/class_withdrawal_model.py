from datetime import date


class ClassWithdrawalModel:
    def __init__(self, course: str, class_id: str, term: str, withdrawal_date: date, grade: str):
        self.course = course
        self.class_id = class_id
        self.term = term
        self.withdrawal_date = withdrawal_date
        self.grade = grade

    def to_dict(self):
        return {
            "course": self.course,
            "class_id": self.class_id,
            "term": self.term,
            "withdrawal_date": self.withdrawal_date,
            "grade": self.grade,
        }
