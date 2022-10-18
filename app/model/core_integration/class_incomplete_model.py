from datetime import date


class ClassIncompleteModel:
    def __init__(self, course: str, class_id: str, term: str, incomplete_date: date, grade: str):
        self.course = course
        self.class_id = class_id
        self.term = term
        self.incomplete_date = incomplete_date
        self.grade = grade

    def to_dict(self):
        return {
            "course": self.course,
            "class_id": self.class_id,
            "term": self.term,
            "incomplete_date": self.incomplete_date,
            "grade": self.grade,
        }
