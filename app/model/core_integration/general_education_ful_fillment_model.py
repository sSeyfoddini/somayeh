from datetime import date


class GeneralEducationFulFillmentModel:
    def __init__(self, recognition_date: date, general_ed: str, term: str):
        self.recognition_date = recognition_date
        self.general_ed = general_ed
        self.term = term

    def to_dict(self):
        return {"recognition_date": self.recognition_date, "general_ed": self.general_ed, "term": self.term}
