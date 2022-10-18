from model.audit_log_model import AuditLogModel

from app import db


class AuditLogPersistence:
    @classmethod
    def add(cls, audit_log):
        db.session.add(audit_log)
        db.session.flush()
        db.session.commit()
        return audit_log

    @classmethod
    def update(cls, audit_log):
        old_audit_log = db.session.query(AuditLogModel).get(audit_log.audit_log_id)
        if old_audit_log is None:
            audit_log = AuditLogPersistence.add(audit_log)
        else:
            old_audit_log.user_id = audit_log.user_id
            old_audit_log.user_name = audit_log.user_name
            old_audit_log.log_date = audit_log.log_date
            old_audit_log.table_name = audit_log.table_name
            old_audit_log.primary_key = audit_log.primary_key
            old_audit_log.dml_type = audit_log.dml_type
            old_audit_log.old_record = audit_log.old_record
            old_audit_log.new_record = audit_log.new_record
            old_audit_log.type = audit_log.type

            db.session.commit()
            audit_log = old_audit_log
        return audit_log

    @classmethod
    def delete(cls, audit_log_id):
        audit_log = db.session.query(AuditLogModel).get(audit_log_id)
        db.session.delete(audit_log)
        db.session.commit()
        return audit_log

    @classmethod
    def get(cls, audit_log_id):
        return db.session.query(AuditLogModel).get(audit_log_id)

    @classmethod
    def get_all(cls):
        return AuditLogModel.query.all()
