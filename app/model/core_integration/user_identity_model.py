class UserIdentitySchemaModel:
    def __init__(self, first_name, last_name, external_id, birth_date, email):
        self.first_name = first_name
        self.last_name = last_name
        self.external_id = external_id
        self.birth_date = birth_date
        self.email = email


    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "external_id": self.external_id,
            "birth_date": self.birth_date,
            "email": self.email,

        }
