from datetime import date


class MillestonCompletionModel:
    def __init__(self, milestone_id: str, milestone_name: str, recognition_date: date, term: str):
        self.milestone_id = milestone_id
        self.milestone_name = milestone_name
        self.recognition_date = recognition_date
        self.term = term

    def to_dict(self):
        return {
            "milestone_id": self.milestone_id,
            "milestone_name": self.milestone_name,
            "recognition_date": self.recognition_date,
            "term": self.term,
        }
