import logging
import os

import requests

from app.model.skill_portfolio_endorsement_model.portfolio_source_model import PortfolioSourceModel
from app.persistence.skill_portfolio_endorsement_persistence.portfolio_source_persistence import (
    PortfolioSourcePersistence,
)
from app.services.issue_params import set_params
from app.util.error_handlers import RecordNotFound


class PortfolioSourceService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        source_credential_id,
        source_credential_label,
        source_portfolio_id,
        type,
        external_id,
    ):

        portfolio_source = PortfolioSourceModel(
            source_credential_id=source_credential_id,
            source_credential_label=source_credential_label,
            source_portfolio_id=source_portfolio_id,
            type=type,
            external_id=external_id,
        )
        portfolio_source = PortfolioSourcePersistence.add(user_id, user_name, portfolio_source)
        return portfolio_source

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        portfolio_source = PortfolioSourcePersistence.get(uuid)

        if portfolio_source is None:
            raise RecordNotFound("'portfolio source' with uuid '{}' not found.".format(uuid))

        portfolio_source = PortfolioSourceModel(
            uuid=uuid,
            source_credential_id=args.get("source_credential_id", portfolio_source.source_credential_id),
            source_credential_label=args.get("source_credential_label", portfolio_source.source_credential_label),
            source_portfolio_id=args.get("source_portfolio_id", portfolio_source.source_portfolio_id),
            type=args.get("type", portfolio_source.type),
            external_id=args.get("external_id", portfolio_source.external_id),
        )
        portfolio_source = PortfolioSourcePersistence.update(user_id, user_name, portfolio_source)

        return portfolio_source

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        portfolio_source = PortfolioSourcePersistence.get(uuid)
        if portfolio_source is None:
            raise RecordNotFound("'portfolio source' with uuid '{}' not found.".format(uuid))
        PortfolioSourcePersistence.delete(user_id, user_name, portfolio_source)
        return portfolio_source

    @classmethod
    def get(cls, uuid):
        portfolio_source = PortfolioSourcePersistence.get(uuid)
        if portfolio_source is None:
            raise RecordNotFound("'portfolio source' with uuid '{}' not found.".format(uuid))
        return portfolio_source

    @classmethod
    def get_all(cls):
        return PortfolioSourcePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return PortfolioSourcePersistence.get_all_by_filter(filter_dict)

    @classmethod
    def issue(cls, external_id: str):
        records = PortfolioSourcePersistence.get_by_external_user_id(external_id)
        pocket_core_api_credential = os.getenv("DATA_BROKER_URL") + "/credential/issue"

        logging.debug(f"Issuing badge credentials for: {external_id} total: {len(records)}")

        for record in records:
            params = set_params(external_id, "portfolio_source", record._to_dict())
            requests.post(pocket_core_api_credential, json=params)
