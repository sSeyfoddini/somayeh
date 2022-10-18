from datetime import date


class ProgramCompletionModel:
    def __init__(self, program_id: str, program_name: str, recognition_date: date, term: str):
        self.program_id = program_id
        self.program_name = program_name
        self.recognition_date = recognition_date
        self.term = term

    def to_dict(self):
        return {
            "program_id": self.program_id,
            "program_name": self.program_name,
            "recognition_date": self.recognition_date,
            "term": self.term,
        }
