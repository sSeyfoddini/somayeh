from datetime import date


class StudentAffiliationModel:
    def __init__(
        self, organization_id: str, organization_name: str, level_id: str, level_name: str, enrollment_date: date
    ):
        self.organization_id = organization_id
        self.organization_name = organization_name
        self.level_id = level_id
        self.level_name = level_name
        self.enrollment_date = enrollment_date

    def to_dict(self):
        return {
            "organization_id": self.organization_id,
            "organization_name": self.organization_name,
            "level_id": self.level_id,
            "level_name": self.level_name,
            "enrollment_date": self.enrollment_date,
        }
