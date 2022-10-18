from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class PortfolioSourceModel(db.Model):
    """
    Data model for PortfolioSource DB table.
    """

    __tablename__ = "portfolio_source"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    source_credential_id = db.Column(db.BIGINT, nullable=False, index=True)
    source_credential_label = db.Column(db.String, nullable=False)
    source_portfolio_id = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "source_credential_id": self.source_credential_id,
            "source_credential_label": self.source_credential_label,
            "source_portfolio_id": self.source_portfolio_id,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return PortfolioSourceModel(
            uuid=self.uuid,
            source_credential_id=self.source_credential_id,
            source_credential_label=self.source_credential_label,
            source_portfolio_id=self.source_portfolio_id,
            type=self.type,
            external_id=self.external_id,
        )
