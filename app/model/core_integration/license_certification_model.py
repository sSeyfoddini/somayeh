from datetime import date


class LicenseCertificationModel:
    def __init__(
        self,
        external_license_certification_id: str,
        license_certification_type_id: str,
        license_certification_name: str,
        program_id: str,
        program_name: str,
        completion_date: date,
        expiration_date: date,
        awards: list,
    ):
        self.external_license_certification_id = external_license_certification_id
        self.license_certification_type_id = license_certification_type_id
        self.license_certification_name = license_certification_name
        self.program_id = program_id
        self.program_name = program_name
        self.completion_date = completion_date
        self.expiration_date = expiration_date
        self.awards = awards

    def to_dict(self):
        return {
            "external_license_certification_id": self.external_license_certification_id,
            "license_certification_type_id": self.license_certification_type_id,
            "license_certification_name": self.license_certification_name,
            "program_id": self.program_id,
            "program_name": self.program_name,
            "completion_date": self.completion_date,
            "expiration_date": self.expiration_date,
            "awards": self.awards,
        }
