import atexit
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app import db
from app.config import Config
from app.model.otp_model import OtpModel
from app.persistence.otp_persistence import OtpPersistence
from app.util.error_handlers import RecordNotFound


class OtpService:
    @classmethod
    def add(cls, email, otp):

        otp = OtpModel(email=email, otp=otp)
        otp = OtpPersistence.add(otp)
        return otp

    @classmethod
    def update(cls, email, otp):
        otp_model = OtpModel(email=email, otp=otp)
        otp_model = OtpPersistence.update(otp_model)

        return otp_model

    @classmethod
    def delete(cls, uuid):
        otp = OtpPersistence.get(uuid)
        if otp is None:
            raise RecordNotFound("'otp' with uuid '{}' not found.".format(uuid))
        OtpPersistence.delete(otp)
        return otp

    @classmethod
    def get(cls, uuid):
        otp = OtpPersistence.get(uuid)
        if otp is None:
            raise RecordNotFound("'otp' with uuid '{}' not found.".format(uuid))
        return otp

    @classmethod
    def get_all(cls):
        return OtpPersistence.get_all()

    @classmethod
    def create_scheduler_app(cls):
        new_app = Flask(__name__, instance_relative_config=False)
        new_app.config.from_object(Config)
        db.init_app(new_app)
        db.app = new_app
        return new_app

    @classmethod
    def scheduler_delete(cls):
        try:
            otps = (
                db.session.query(OtpModel).filter(OtpModel.created_at <= datetime.now() - timedelta(minutes=15)).all()
            )
        except Exception as e:
            print("message    ", e.args)
        for otp in otps:
            db.session.delete(otp)

        db.session.commit()

    @classmethod
    def scheduler(cls):
        cls.create_scheduler_app()
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=cls.scheduler_delete, trigger="interval", minutes=15)
        scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

    @classmethod
    def get_by_mail(cls, email):
        return OtpPersistence.get_by_email(email)
