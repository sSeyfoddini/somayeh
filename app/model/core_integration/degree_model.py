from datetime import date


class DegreeModel:
    def __init__(
        self,
        id: str,
        degree_type_id: str,
        external_degree_id: str,
        degree_name: str,
        institution_name: str,
        college_name: str,
        program_id: str,
        program_name: str,
        completion_date: date,
        awards: list,
        attachment: str,
    ):
        self.id = id
        self.degree_type_id = degree_type_id
        self.external_degree_id = external_degree_id
        self.degree_name = degree_name
        self.institution_name = institution_name
        self.college_name = college_name
        self.program_id = program_id
        self.program_name = program_name
        self.completion_date = completion_date
        self.awards = awards
        self.attachment = attachment

    def to_dict(self):
        return {
            "id": self.id,
            "degree_type_id": self.degree_type_id,
            "external_degree_id": self.external_degree_id,
            "degree_name": self.degree_name,
            "institution_name": self.institution_name,
            "college_name": self.college_name,
            "program_id": self.program_id,
            "program_name": self.program_name,
            "completion_date": self.completion_date,
            "awards": self.awards,
            "attachment": self.attachment,
        }
