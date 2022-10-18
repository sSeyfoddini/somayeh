from datetime import date


class TranscriptModel:
    def __init__(
        self,
        transcript_id: str,
        credential_name: str,
        collection_id: str,
        issue_date: date,
        institution_name: str,
        attachments: list,
    ):
        self.transcript_id = transcript_id
        self.credential_name = credential_name
        self.collection_id = collection_id
        self.issue_date = issue_date
        self.institution_name = institution_name
        self.attachments = attachments

    def to_dict(self):
        return {
            "transcript_id": self.transcript_id,
            "credential_name": self.credential_name,
            "collection_id": self.collection_id,
            "issue_date": self.issue_date,
            "institution_name": self.institution_name,
            "attachments": self.attachments,
        }
