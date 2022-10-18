import requests


class BadgrService:

    @classmethod
    def authanticate(cls, username, password):
        pocket_authentication = "https://api.badgr.io/o/token"
        PARAMS = {"username": username, "password": password}
        auth = requests.post(pocket_authentication, data=PARAMS)
        text = auth.json()
        return text["access_token"], text["refresh_token"]

    @classmethod
    def get_issusers(cls, token):
        uri = "https://api.badgr.io/v2/issuers"
        hed = {"Authorization": "Bearer " + token}

        response = requests.get(uri, headers=hed)
        result = response.json()
        return result["result"]

    @classmethod
    def get_issusers_entityid(cls, token):
        uri = "https://api.badgr.io/v2/issuers"
        hed = {"Authorization": "Bearer " + token}

        response = requests.get(uri, headers=hed)
        text = response.json()
        entityId = []
        for item in text["result"]:
            entityId.append(item["entityId"])
        return entityId

    @classmethod
    def badge_get_all_badges(cls, token, entityId):
        hed = {"Authorization": "Bearer " + token}
        responses = []
        for i in entityId:
            uri = "https://api.badgr.io/v2/issuers/" + i + "/assertions"
            response = requests.get(uri, headers=hed)
            responses.append(response.json()["result"])
        return responses

    @classmethod
    def get_badge_by_email(cls, token, entityId, email):
        hed = {"Authorization": "Bearer " + token}
        responses = []
        for i in entityId:
            uri = "https://api.badgr.io/v2/issuers/" + i + "/assertions"
            response = requests.get(uri, headers=hed)
            responses.append(response.json())
        information = []
        for item in responses:
            for i in item["result"]:
                if i["recipient"]["plaintextIdentity"] == email:
                    information.append(i)

        return information

    @classmethod
    def badge_type_get_all_badges(cls, token, entityId):
        hed = {"Authorization": "Bearer " + token}
        responses = []
        for i in entityId:
            uri = "https://api.badgr.io/v2/issuers/" + i + "/badgeclasses"
            response = requests.get(uri, headers=hed)
            responses.append(response.json()["result"])
        return responses

    @classmethod
    def insert_in_badgr(cls, badge_type, email, token):
        print("Insert badge to badger")
        issuer = badge_type["issuer"]
        url = f"https://api.badgr.io/v2/issuers/{issuer}/assertions"

        body = {
            "badgeclass": badge_type["entityId"],
            "issuer": issuer,
            "issuerOpenBadgeId": badge_type["issuerOpenBadgeId"],
            "recipient": {
                "identity": email,
                "hashed": True,
                "type": "email",
                "plaintextIdentity": "string",
                "salt": "string"
            },
            "narrative": "string",
            "evidence": [
            ]
        }

        hed = {"Authorization": "Bearer " + token}
        response = requests.post(url, json=body, headers=hed)
        if response.status_code == 201:
            return response.json()["result"][0]
        return None