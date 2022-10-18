import requests

from app.config import Config
import logging

_log = logging.getLogger(__name__)

class SetExternalId:
    @classmethod
    def set_external_id(cls, connection_id, external_id):
        _log.info(f"Setting external id for connection_id: {connection_id}")
        print(f"Setting external id for connection_id: {connection_id}")
        result = requests.put(
            Config.pocket_core_api_set_external_id, json={"connection_id": connection_id, "external_id": external_id}
        )
