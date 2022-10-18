from app import db


class AuditLogModel(db.Model):
    __tablename__ = "audit_log"

    audit_log_id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT)
    user_name = db.Column(db.String(75))
    log_date = db.Column(db.DateTime(timezone=False), nullable=False)
    table_name = db.Column(db.String(130), nullable=False)
    primary_key = db.Column(db.String(255), nullable=False)
    dml_type = db.Column(db.String(20), nullable=False)
    old_record = db.Column(db.JSON)
    new_record = db.Column(db.JSON)

    def _to_dict(self):
        return {
            "audit_log_id": self.audit_log_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "log_date": str(self.log_date),
            "table_name": self.table_name,
            "primary_key": self.primary_key,
            "dml_type": self.dml_type,
            "old_record": self.old_record,
            "new_record": self.new_record,
        }

    def _clone(self):
        return AuditLogModel(
            audit_log_id=self.audit_log_id,
            user_id=self.user_id,
            user_name=self.user_name,
            log_date=self.log_date,
            table_name=self.table_name,
            primary_key=self.primary_key,
            dml_type=self.dml_type,
            old_record=self.old_record,
            new_record=self.new_record,
        )

    @classmethod
    def audit_log(
        cls,
        user_id,
        user_name,
        log_date,
        table_name,
        primary_key,
        dml_type,
        old_record_json,
        new_record_json,
    ):
        audit_log = AuditLogModel(
            user_id=user_id,
            user_name=user_name,
            log_date=log_date,
            table_name=table_name,
            primary_key=str(primary_key),
            dml_type=dml_type,
            old_record=(db.JSON.NULL if old_record_json is None else old_record_json),
            new_record=(db.JSON.NULL if new_record_json is None else new_record_json),
        )
        return audit_log
