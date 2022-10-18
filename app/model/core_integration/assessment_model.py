from datetime import date


class AssessmentModel:
    def __init__(self, name: str, date: date):
        self.name = name
        self.date = date

    def to_dict(self):
        return {"name": self.name, "date": self.date}
