from datetime import date


class CertificateModel:
    def __init__(
        self,
        certificate_type_id: str,
        certificate_name: str,
        program_name: str,
        completion_date: date,
        awards: list,
        attachment: str,
    ):
        self.certificate_type_id = certificate_type_id
        self.certificate_name = certificate_name
        self.program_name = program_name
        self.completion_date = completion_date
        self.awards = awards
        self.attachment = attachment

    def to_dict(self):
        return {
            "certificate_type_id": self.certificate_type_id,
            "certificate_name": self.certificate_name,
            "program_name": self.program_name,
            "completion_date": self.completion_date,
            "awards": self.awards,
            "attachment": self.attachment,
        }
