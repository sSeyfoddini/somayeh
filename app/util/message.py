from pathlib import Path

import yaml


def get_message(lang, code):

    default_message = ""
    default_content = Path("content/Message.yml")
    try:
        with open(default_content, encoding="utf-8") as file:
            documents = yaml.full_load(file)
            default_message = documents.get(code)
        if default_message is None:
            raise Exception
    except Exception:
        default_message = ""

    message = ""
    content = Path("content/Message_" + lang.lower() + ".yml")
    try:
        with open(content, encoding="utf-8") as file:
            documents = yaml.full_load(file)
            message = documents.get(code)
        if message is None:
            raise Exception
    except Exception:
        message = default_message

    return message


def contains_message(lang, code):
    msg = get_message(lang, code)
    if msg == "":
        return False
    else:
        return True
