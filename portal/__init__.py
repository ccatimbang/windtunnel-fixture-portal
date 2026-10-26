"""Fixture Portal: a small test site whose pages are kept for some of its accounts.

Three accounts sign in at /login: admin, manager, and member. Every signed-in page is behind login_required; the
reports and the team behind manager_required, which admins pass too; the admin pages behind admin_required. Two
pages, /reports/team and /admin/audit, are linked from no page.
"""

from flask import Flask

from portal.account import account
from portal.admin import admin
from portal.auth import auth
from portal.public import public
from portal.reports import reports


def create_app() -> Flask:
    app = Flask(__name__)
    # A fixture's own session key: it signs the cookies of three made-up accounts on a local site.
    app.config["SECRET_KEY"] = "fixture-portal-session-key"
    app.register_blueprint(public)
    app.register_blueprint(auth)
    app.register_blueprint(account, url_prefix="/account")
    app.register_blueprint(reports, url_prefix="/reports")
    app.register_blueprint(admin, url_prefix="/admin")
    return app
