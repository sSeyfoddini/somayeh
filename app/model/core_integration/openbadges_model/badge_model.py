class BadgeModel:
    def __init__(self, achievement_type: str, name: str, description: str, image: str, credential_subject: str):
        self.achievement_type = achievement_type
        self.name = name
        self.description = description
        self.image = image
        self.credential_subject = credential_subject

    def to_dict(self):
        return {
            "achievement_type": self.achievement_type,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "credential_subject": self.credential_subject,
        }
