from pathlib import Path

import yaml


def get_param(key):
    value = ""
    default_content = Path("param.yml")
    try:
        with open(default_content, encoding="utf-8") as file:
            documents = yaml.full_load(file)
            value = documents.get(key)
        if value is None:
            raise Exception
    except Exception:
        value = ""
    return value
