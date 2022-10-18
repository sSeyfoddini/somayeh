class ImageModel:
    def __init__(self, caption: str):
        self.caption = caption

    def to_dict(self):
        return {"caption": self.caption}
