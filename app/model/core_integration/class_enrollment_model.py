from datetime import date


class ClassEnrollmentModel:
    def __init__(self, course: str, class_id: str, term: str, enrollment_date: date, roster_id: str):
        self.course = course
        self.class_id = class_id
        self.term = term
        self.enrollment_date = enrollment_date
        self.roster_id = roster_id

    def to_dict(self):
        return {
            "course": self.course,
            "class_id": self.class_id,
            "term": self.term,
            "enrollment_date": self.enrollment_date,
            "roster_id": self.roster_id,
        }
