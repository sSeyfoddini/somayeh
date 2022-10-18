class TermModel:
    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {"name": self.name}
