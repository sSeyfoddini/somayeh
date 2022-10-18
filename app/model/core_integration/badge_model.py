from datetime import date


class BadgeModel:
    def __init__(self, award_type_id: str, label: str, award_date: str, badge_description: str, badge_image: str, url: str):
        self.award_type_id = award_type_id
        self.label = label
        self.award_date = award_date
        self.badge_description = badge_description
        self.badge_image = badge_image
        self.url = url

    def to_dict(self):
        return {"award_type_id": self.award_type_id, "label": self.label, "award_date": self.award_date, "badge_description": self.badge_description, "badge_image": self.badge_image, "url": self.url}
