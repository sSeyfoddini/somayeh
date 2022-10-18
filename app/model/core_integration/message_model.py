class MessageRequest:
    def __init__(self, data_dict: dict):
        # self.connection_external_id = data_dict["connection_external_id"]
        self.connection_id = data_dict["connection_id"]
        self.message_body = MessageBody(data_dict["message_body"])


class MessageBody:
    def __init__(self, data_dict: dict):
        self.type = data_dict.get("type", "")
        self.key = data_dict.get("key", "")
        self.email = data_dict.get("email", "")
        self.first_name = data_dict.get("first_name", "")
        self.last_name = data_dict.get("last_name", "")
        self.email = data_dict.get("email", "")
        self.code = data_dict.get("code", "")
        self.consent_acceptance = data_dict.get("consent_acceptance", "")
        self.badge_id = data_dict.get("badge_id", "")
