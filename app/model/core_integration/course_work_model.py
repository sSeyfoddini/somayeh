class CourseWorkModel:
    def __init__(
        self,
        coursework_type_id: str,
        coursework_type_name: str,
        class_id: str,
        course: str,
        external_assignment_id: str,
        name: str,
        description: str,
        possible_points: str,
        points: str,
        refererence_uri: str,
        attachment: str,
        class_enrollment_id: str,
    ):
        self.coursework_type_id = coursework_type_id
        self.coursework_type_name = coursework_type_name
        self.class_id = class_id
        self.course = course
        self.external_assignment_id = external_assignment_id
        self.name = name
        self.description = description
        self.possible_points = possible_points
        self.points = points
        self.refererence_uri = refererence_uri
        self.attachment = attachment
        self.class_enrollment_id = class_enrollment_id

    def to_dict(self):
        return {
            "coursework_type_id": self.coursework_type_id,
            "coursework_type_name": self.coursework_type_name,
            "class_id": self.class_id,
            "course": self.course,
            "external_assignment_id": self.external_assignment_id,
            "name": self.name,
            "description": self.description,
            "possible_points": self.possible_points,
            "points": self.points,
            "refererence_uri": self.refererence_uri,
            "attachment": self.attachment,
            "class_enrollment_id": self.class_enrollment_id,
        }
