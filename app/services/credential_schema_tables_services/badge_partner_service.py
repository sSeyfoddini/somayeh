
from app.model.credential_schema_tables_model.badge_partner_model import BadgePartnerModel
from app.persistence.credential_schema_tables_persistence.badge_partner_persistence import BadgePartnerPersistence
from app.util.error_handlers import RecordNotFound


class BadgePartnerService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        name,
        url
    ):

        badge_partner = BadgePartnerModel(
            name=name,
            url=url
        )
        badge_partner = BadgePartnerPersistence.add(user_id, user_name, badge_partner)
        return badge_partner

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        badge_partner = BadgePartnerPersistence.get(uuid)

        if badge_partner is None:
            raise RecordNotFound("'badge_partner' with uuid '{}' not found.".format(uuid))

        badge_partner = BadgePartnerModel(
            uuid=uuid,
            name=args.get("name", badge_partner.name),
            url=args.get("url", badge_partner.url)
        )
        badge_partner = BadgePartnerPersistence.update(user_id, user_name, badge_partner)

        return badge_partner

    @classmethod
    def delete_all(cls):
        BadgePartnerPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        badge_partner = BadgePartnerPersistence.get(uuid)
        if badge_partner is None:
            raise RecordNotFound("'badge_partner' with uuid '{}' not found.".format(uuid))
        BadgePartnerPersistence.delete(user_id, user_name, badge_partner)
        return badge_partner

    @classmethod
    def get(cls, uuid):
        badge_partner = BadgePartnerPersistence.get(uuid)
        if badge_partner is None:
            raise RecordNotFound("'badge_partner' with uuid '{}' not found.".format(uuid))
        return badge_partner

    @classmethod
    def get_all(cls):
        return BadgePartnerPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        return BadgePartnerPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def get_by_url(cls, url):
        badge_partner = BadgePartnerPersistence.get_by_url(url)
        if badge_partner is None:
            raise RecordNotFound("'badge_partner' with url '{}' not found.".format(url))
        return badge_partner