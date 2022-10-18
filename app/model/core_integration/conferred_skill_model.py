class ConferredSkillModel:
    def __init__(self, label: str):
        self.label = label

    def to_dict(self):
        return {"label": self.label}
