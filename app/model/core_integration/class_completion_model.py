from datetime import date


class ClassCompletionModel:
    def __init__(
        self,
        course: str,
        class_id: str,
        completion_date: date,
        term: str,
        grade: str,
        credits: int,
        general_ed: str,
        program_fulfill: bool,
        conferred_skills: list,
    ):
        self.course = course
        self.class_id = class_id
        self.completion_date = completion_date
        self.term = term
        self.grade = grade
        self.credits = credits
        self.general_ed = general_ed
        self.program_fulfill = program_fulfill
        self.conferred_skills = conferred_skills

    def to_dict(self):
        return {
            "course": self.course,
            "class_id": self.class_id,
            "program_name": self.program_name,
            "completion_date": self.completion_date,
            "term": self.term,
            "grade": self.grade,
            "credits": self.credits,
            "general_ed": self.general_ed,
            "program_fulfill": self.program_fulfill,
            "conferred_skills": self.conferred_skills,
        }
