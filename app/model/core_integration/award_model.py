from datetime import date


class AwardModel:
    def __init__(self, award_type_id: str, label: str, award_date: date):
        self.award_type_id = award_type_id
        self.label = label
        self.award_date = award_date

    def to_dict(self):
        return {"award_type_id": self.award_type_id, "label": self.label, "award_date": self.award_date}
