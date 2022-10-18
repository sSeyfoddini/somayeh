import os

import pandas as pd
import requests

from app import db
from app.config import Config
from app.model.skill_portfolio_endorsement_model.skill_type_model import SkillTypeModel
from app.services.skill_portfolio_endorsement_services.skill_type_service import SkillTypeService


class EmsiService:
    @classmethod
    def get_skills(cls):
        ROOT_DIR = os.path.abspath(os.curdir)
        REL_PATH = "resources/SkillsTables.xlsx"
        FILE_PATH = os.path.join(ROOT_DIR, REL_PATH)
        access_token = cls.get_token()
        url = "https://emsiservices.com/skills/versions/latest/skills"

        headers = {"Authorization": "Bearer " + access_token}

        response = requests.request("GET", url, headers=headers).json()

        db.session.query(SkillTypeModel).delete()

        user_id = 1
        username = "test"
        for data in response["data"]:
            skill_type = SkillTypeService.add(
                user_id=user_id,
                user_name=username,
                name=data["name"],
                description="",
                category_id=[],
                category_name=[],
                Updates_for_POCKMMVP_1030="",
                reference_url=data["infoUrl"],
                source_skill_type_id=data["id"],
                occupation_ids="",
                employer_ids="",
                keywords=[],
                rsd="",
                rsd_uri="",
            )

        df = pd.read_excel(FILE_PATH, sheet_name="skills")
        file_datas = df.values.tolist()

        for data in file_datas:
            reference_url = data[6]
            if reference_url and type(reference_url) is str:
                skill_type = SkillTypeService.get_by_reference_url(reference_url)
                if skill_type:
                    skill_type = SkillTypeService.update(
                        user_id=user_id,
                        user_name=username,
                        id=skill_type.id,
                        name=skill_type.name,
                        description=data[2] if type(data[2]) is str else "",
                        category_id=skill_type.category_id,
                        category_name=[data[4]] if type(data[4]) is str else [],
                        Updates_for_POCKMMVP_1030=data[5] if type(data[5]) is str else "",
                        reference_url=skill_type.reference_url,
                        source_skill_type_id=skill_type.source_skill_type_id,
                        occupation_ids=skill_type.occupation_ids,
                        employer_ids=skill_type.employer_ids,
                        keywords=data[7].split(",") if type(data[7]) is str else [],
                        rsd=skill_type.rsd,
                        rsd_uri=skill_type.rsd_uri,
                    )
                else:
                    skill_type = SkillTypeService.add(
                        user_id=user_id,
                        user_name=username,
                        name="",
                        description=data[2] if type(data[2]) is str else "",
                        category_id=[],
                        category_name=[data[4]] if type(data[4]) is str else [],
                        Updates_for_POCKMMVP_1030=data[5] if type(data[5]) is str else "",
                        reference_url=reference_url,
                        source_skill_type_id="",
                        occupation_ids="",
                        employer_ids="",
                        keywords=data[7].split(",") if type(data[7]) is str else [],
                        rsd="",
                        rsd_uri="",
                    )

    @classmethod
    def get_token(cls):
        CLIENT_ID = Config.EMSI_CLIENT_ID
        CLIENT_SECRET = Config.EMSI_CLIENT_SECRET
        SCOPE = Config.EMSI_SCOPE
        url = "https://auth.emsicloud.com/connect/token"

        payload = f"client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials&scope={SCOPE}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.json()["access_token"]
