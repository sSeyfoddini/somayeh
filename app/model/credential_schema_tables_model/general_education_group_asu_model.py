from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class GeneralEducationGroupASUModel(db.Model):
    """
    Data model for GeneralEducation DB table.
    """

    __tablename__ = "general_education_group_asu"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)
    gen_id_list = db.Column(db.BIGINT, nullable=True, index=True)
    gen_code_list = db.Column(db.String, nullable=False)
    credential_type_id = db.Column(db.String, nullable=True)
    parent_organization = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "external_id": self.external_id,
            "gen_id_list": self.gen_id_list,
            "gen_code_list": self.gen_code_list,
            "credential_type_id": self.credential_type_id,
            "parent_organization": self.parent_organization,
        }

    def _clone(self):
        return GeneralEducationGroupASUModel(
            name=self.name,
            description=self.description,
            external_id=self.external_id,
            gen_id_list=self.gen_id_list,
            gen_code_list=self.gen_code_list,
            credential_type_id=self.credential_type_id,
            parent_organization=self.parent_organization,
            uuid=self.uuid,
        )
