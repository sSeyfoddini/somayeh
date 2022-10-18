from datetime import date


class ProgramAffiliationModel:
    def __init__(
        self,
        program_external_id: str,
        program_type_name: str,
        parent_id: str,
        program_id: str,
        program_name: str,
        parent_name: str,
        date: date,
    ):
        self.program_external_id = program_external_id
        self.program_type_name = program_type_name
        self.parent_id = parent_id
        self.program_id = program_id
        self.program_name = program_name
        self.parent_name = parent_name
        self.date = date

    def to_dict(self):
        return {
            "program_external_id": self.program_external_id,
            "program_type_name": self.program_type_name,
            "parent_id": self.parent_id,
            "program_id": self.program_id,
            "program_name": self.program_name,
            "parent_name": self.parent_name,
            "date": self.date,
        }
