from datetime import date


class CollageAffiliationModel:
    def __init__(self, college_id: str, college_name: str, parent_id: str, parent_name: str, date: date):
        self.college_id = college_id
        self.college_name = college_name
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.date = date

    def to_dict(self):
        return {
            "college_id": self.college_id,
            "college_name": self.college_name,
            "parent_id": self.parent_id,
            "parent_name": self.parent_name,
            "date": self.date,
        }
