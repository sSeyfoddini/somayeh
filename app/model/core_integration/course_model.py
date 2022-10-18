class CourseModel:
    def __init__(self, class_id: str, subject: str, number: str):
        self.class_id = class_id
        self.subject = subject
        self.number = number

    def to_dict(self):
        return {"class_id": self.class_id, "subject": self.subject, "number": self.number}
