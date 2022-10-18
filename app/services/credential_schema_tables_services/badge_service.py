import datetime

from app.model.credential_schema_tables_model.badge_model import BadgeModel
from app.persistence.credential_schema_tables_persistence.badge_persistence import BadgePersistence
from app.services.core_integration.issue_badge import IssueBadge
from app.services.credential_schema_tables_services.badge_type_service import BadgeTypeService
from app.services.learners_service import LearnersService
from app.config import Config
from app.services.badgr_service import BadgrService
from app.model.core_integration.badge_model import BadgeModel as BadgeModelIssue
from app.util.error_handlers import RecordNotFound


class BadgeService:
    @classmethod
    def add(
            cls,
            user_id,
            user_name,
            credential_type_id,
            credential_type_label,
            class_id,
            external_user_id,
            badge_type_uuid,
            badge_name,
            badge_description,
            badge_org_id,
            badge_org_label,
            badge_org_logo,
            badge_date,
            badge_external_link,
            badge_json,
            key,
            learner_uuid
    ):
        badge_image = ""
        badge_type = None
        if badge_type_uuid:
            badge_type = BadgeTypeService.get(badge_type_uuid)
            if badge_type.image:
                badge_image = badge_type.image

        badge = BadgeModel(
            credential_type_id=credential_type_id ,
            credential_type_label=credential_type_label,
            class_id=class_id,
            external_user_id=external_user_id,
            badge_type_uuid=badge_type_uuid,
            badge_name=badge_name,
            badge_description=badge_description,
            badge_org_id=badge_org_id,
            badge_org_label=badge_org_label,
            badge_org_logo=badge_org_logo,
            badge_date=badge_date,
            badge_external_link=badge_external_link,
            badge_image=badge_image,
            badge_json=badge_json,
            key=key,
            learner_uuid=learner_uuid
        )

        badge = BadgePersistence.add(user_id, user_name, badge)

        if badge_type and badge_type.extrernal_partner_label == "badgr":
            issue_badge = BadgeModelIssue(badge.uuid, badge.badge_name, str(datetime.datetime.now()),
                                     badge.badge_description
                                     , badge.badge_image, badge.badge_external_link)
            IssueBadge.issue_badge(badge.learner_uuid, issue_badge)

        return badge

    @classmethod
    def update(cls,user_id, user_name, uuid, args):
        badge = BadgePersistence.get(uuid)

        if badge is None:
            raise RecordNotFound("'badge' with uuid '{}' not found.".format(uuid))

        badge_image = ""
        badge_type = None
        if "badge_type_uuid" in args and args["badge_type_uuid"]:
            badge_type = BadgeTypeService.get(args["badge_type_uuid"])
            if badge_type.image:
                badge_image = badge_type.image

        else:
            badge_image = badge.badge_image
        badge = BadgeModel(
            uuid=uuid,
            credential_type_id=args.get("credential_type_id", badge.credential_type_id),
            credential_type_label=args.get("credential_type_label", badge.credential_type_label),
            class_id=args.get("class_id", badge.class_id),
            external_user_id=args.get("external_user_id", badge.external_user_id),
            badge_type_uuid=args.get("badge_type_uuid", badge.badge_type_uuid),
            badge_name=args.get("badge_name", badge.badge_name),
            badge_description=args.get("badge_description", badge.badge_description),
            badge_org_id=args.get("badge_org_id", badge.badge_org_id),
            badge_org_label=args.get("badge_org_label", badge.badge_org_label),
            badge_org_logo=args.get("badge_org_logo", badge.badge_org_logo),
            badge_date=args.get("badge_date", badge.badge_date),
            badge_external_link=args.get("badge_external_link", badge.badge_external_link),
            badge_image=badge_image,
            badge_json=args.get("badge_json", badge.badge_json),
            key=args.get("key", badge.key),
            learner_uuid=args.get("learner_uuid", badge.learner_uuid),
        )
        badge = BadgePersistence.update(user_id, user_name, badge)

        if badge_type and badge_type.extrernal_partner_label == "badgr":
            issue_badge = BadgeModelIssue(badge.uuid, badge.badge_name, str(datetime.datetime.now()),
                                     badge.badge_description
                                     , badge.badge_image, badge.badge_external_link)
            IssueBadge.issue_badge(badge.learner_uuid, issue_badge)

        return None, badge

    @classmethod
    def delete_all(cls):
        BadgePersistence.delete_all()

    @classmethod
    def delete(cls, user_id, user_name, uuid):
        badge = BadgePersistence.get(uuid)
        if badge is None:
            raise RecordNotFound("'badge' with uuid '{}' not found.".format(uuid))
        BadgePersistence.delete(user_id, user_name, badge)

    @classmethod
    def get(cls, uuid):
        badge = BadgePersistence.get(uuid)
        if badge is None:
            raise RecordNotFound("'badge' with uuid '{}' not found.".format(uuid))
        return badge

    @classmethod
    def get_all(cls):
        return BadgePersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict, only_uuid=False):
        badges = BadgePersistence.get_all_by_filter(filter_dict)
        if only_uuid:
            uuid = []
            for badge in badges[0]:
                uuid.append(badge.uuid)
            return uuid, badges[1], badges[2]
        return badges

    @classmethod
    def get_by_badge_external_link(cls, link: str):
        return BadgePersistence.get_by_badge_external_link(link)

    @classmethod
    def get_all_from_badgr(cls):
        username = Config.BADGER_USERNAME
        password = Config.BADGER_PASSWORD

        access_token, refresh_token = BadgrService.authanticate(username, password)
        entity_id = BadgrService.get_issusers_entityid(access_token)
        result = BadgrService.badge_get_all_badges(access_token, entity_id)

        user_id = 1
        username = "test"

        for badges in result:
            for badge in badges:
                email = badge['recipient']['identity']
                learner = LearnersService.get_by_email(email)
                old_badge = BadgeService.get_by_badge_external_link(badge["openBadgeId"])
                if learner and not old_badge:
                    badge_type = BadgeTypeService.get_all_by_filter({"name": "Onboarded to ASU with Pocket"})[0][0]
                    BadgeService.add(
                        user_id=user_id,
                        user_name=username,
                        credential_type_id="96a91f49-f3a2-45b7-8114-74da5fa8682f",
                        credential_type_label="general_education_group_asu",
                        class_id=badge["badgeclass"],
                        external_user_id="",
                        badge_type_uuid=badge_type.uuid,
                        badge_name=badge_type.name,
                        badge_description="",
                        badge_org_id="67abcf62-0be9-4204-8822-325992f6857b",
                        badge_org_label="ASU",
                        badge_org_logo="",
                        badge_date="",
                        badge_external_link=badge["openBadgeId"],
                        badge_json={},
                        key="",
                        learner_uuid=learner.uuid
                    )

    @classmethod
    def get_true_auto_issue_badges(cls, email):
        learner = LearnersService.get_by_email(email)
        badges, total_records, page= cls.get_all_by_filter({"learner_uuid": learner.uuid})

        auto_issue_badges=[]

        for badge in badges:
            if badge.badge_type_uuid:
                badge_type = BadgeTypeService.get(badge.badge_type_uuid)
                if badge_type.auto_issue:
                    auto_issue_badges.append(badge)

        return auto_issue_badges