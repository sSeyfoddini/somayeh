class AchievementSubjectModel:
    def __init__(self, type: str, achievement_type: str):
        self.type = type
        self.achievement_type = achievement_type

    def to_dict(self):
        return {"type": self.type, "achievement_type": self.achievement_type}
