from app.persistence import get_models


class FieldsDefinitionService:
    @classmethod
    def get(cls, table_name):
        datas = {}
        classes, models, table_names = get_models()

        for model in classes:
            if table_name == model.__tablename__:
                for c in model.__table__.columns:
                    datas.update(
                        {
                            str(c.name): {
                                "type": str(c.type.python_type)[8:-2],
                                "required": not c.nullable,
                            }
                        }
                    )

        return datas

