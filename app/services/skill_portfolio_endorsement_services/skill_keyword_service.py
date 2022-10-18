
from app.model.skill_portfolio_endorsement_model.skill_keyword_model import SkillKeywordModel
from app.persistence.skill_portfolio_endorsement_persistence.skill_keyword_persistence import SkillKeywordPersistence
from app.util.error_handlers import RecordNotFound


class SkillKeywordService:
    @classmethod
    def add(cls, user_id, user_name, keyword):

        skill_keyword = SkillKeywordModel(keyword=keyword)
        skill_keyword = SkillKeywordPersistence.add(user_id, user_name, skill_keyword)
        return skill_keyword

    @classmethod
    def update(cls, user_id, user_name, keyword, uuid):
        skill_keyword = SkillKeywordPersistence.get(uuid)

        if skill_keyword is None:
            raise RecordNotFound("'skill keyword' with uuid '{}' not found.".format(uuid))

        skill_keyword = SkillKeywordModel(keyword=keyword, uuid=uuid)
        skill_keyword = SkillKeywordPersistence.update(user_id, user_name, skill_keyword)

        return skill_keyword

    @classmethod
    def delete(cls, user_id, user_name, skill_keyword):
        SkillKeywordPersistence.delete(user_id, user_name, skill_keyword)
        return skill_keyword

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        skill_keyword = SkillKeywordPersistence.get(uuid)
        if skill_keyword is None:
            raise RecordNotFound("'skill keyword' with uuid '{}' not found.".format(uuid))
        SkillKeywordPersistence.delete(user_id, user_name, skill_keyword)
        return skill_keyword

    @classmethod
    def get(cls, uuid):
        skill_keyword = SkillKeywordPersistence.get(uuid)
        if skill_keyword is None:
            raise RecordNotFound("'skill keyword' with uuid '{}' not found.".format(uuid))
        return skill_keyword

    @classmethod
    def get_all(cls):
        return SkillKeywordPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return SkillKeywordPersistence.get_all_by_filter(filter_dict)

