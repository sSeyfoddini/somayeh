class GradeModel:
    def __init__(self, label: str, value: int):
        self.label = label
        self.value = value

    def to_dict(self):
        return {"label": self.label, "value": self.value}
