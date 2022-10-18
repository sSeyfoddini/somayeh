from app.persistence import get_models
from dateutil.parser import parse
from datetime import datetime
from app.util.error_handlers import InvalidField

class CheckField:
    @classmethod
    def check_missing_field_and_field_type(cls, table_name, request_fields):
        essential_fields, fields_type = cls.get_essential_fields_and_fields_type(table_name)

        # check essential fields
        for key in essential_fields:
            if key not in request_fields.keys():
                raise InvalidField("Missing field '{}'".format(key))

        # check fields type
        for key, val in request_fields.items():
            if type(val) is not fields_type[key]:
                if type(val) is str:
                    is_date = cls.is_date(val)
                    if is_date and fields_type[key] is datetime:
                        continue
                elif type(val) is list and fields_type[key] is str:
                    continue

                raise InvalidField(
                    "Invalid field type. The '{}' type should be {}.".format(key, str(fields_type[key])[7:-1])
                )


    @classmethod
    def is_date(cls, string):
        try:
            parse(string, fuzzy=False)
            return True

        except ValueError:
            return False

    @classmethod
    def get_essential_fields_and_fields_type(cls, table_name):
        fields_type = {}
        essential_fields = []
        classes, models, table_names = get_models()

        for model in classes:
            if table_name == model.__tablename__:
                for c in model.__table__.columns:
                    if not c.nullable:
                        if not c.default and c.autoincrement == "auto":
                            essential_fields.append(str(c.name))
                    fields_type[str(c.name)] = c.type.python_type
        return essential_fields, fields_type