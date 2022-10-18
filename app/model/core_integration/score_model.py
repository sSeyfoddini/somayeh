class ScoreModel:
    def __init__(
        self,
        assessment: str,
        score: int,
        score_total: int,
        certificate_id: str,
        certificate_name: str,
        issuing_organization_id: str,
        issuing_organization_name: str,
        recognized_organization_id: list,
    ):
        self.assessment = assessment
        self.score = score
        self.score_total = score_total
        self.certificate_id = certificate_id
        self.certificate_name = certificate_name
        self.issuing_organization_id = issuing_organization_id
        self.issuing_organization_name = issuing_organization_name
        self.recognized_organization_id = recognized_organization_id

    def to_dict(self):
        return {
            "assessment": self.assessment,
            "score": self.score,
            "score_total": self.score_total,
            "certificate_id": self.certificate_id,
            "certificate_name": self.certificate_name,
            "issuing_organization_id": self.issuing_organization_id,
            "issuing_organization_name": self.issuing_organization_name,
            "recognized_organization_id": self.recognized_organization_id,
        }
