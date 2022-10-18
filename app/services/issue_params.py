import uuid


def set_params(external_id: str, external_schema_id: str, attributes: dict):

    PARAMS = {
        "external_connection_id": external_id,
        "external_schema_id": external_schema_id,
        "credential_id": str(uuid.uuid4())[:8] + "-" + external_id,
        "comment": "",
        "attributes": attributes,
    }
    return PARAMS
