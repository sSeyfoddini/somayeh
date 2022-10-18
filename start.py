"""App entry point."""

import sys

from flask_cors import CORS
from flask_migrate import Migrate

from app import db
from app.create_app import create_app
from app.services.otp_service import OtpService
from command import (
    organization,
    colleges,
    course,
    credential_type,
    export,
    general,
    organization_identity,
    program,
    role,
    skill_type,
    term,
    learner_insert,
    learner_update,
    badge_type_get_all_from_badgr,
    badge_get_all_from_badgr,
    _class
)

app = create_app()
OtpService.scheduler()
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/*": {"origins": "*"}})

app.cli.add_command(export)
app.cli.add_command(organization_identity,"organization_identity")
app.cli.add_command(organization)
app.cli.add_command(colleges)
app.cli.add_command(term)
app.cli.add_command(program)
app.cli.add_command(course)
app.cli.add_command(general)
app.cli.add_command(role)
app.cli.add_command(credential_type, "credential_type")
app.cli.add_command(skill_type)
app.cli.add_command(learner_insert, "learners_insert")
app.cli.add_command(learner_update, "learners_update")
app.cli.add_command(badge_type_get_all_from_badgr, "badge_type_get_all")
app.cli.add_command(badge_get_all_from_badgr, "badge_get_all")
app.cli.add_command(_class, "class")


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    return response


migrate = Migrate(app, db)

# with app.app_context():
#
#     db.drop_all()
#     db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
