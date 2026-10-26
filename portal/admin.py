from flask import Blueprint, jsonify, render_template

from portal.auth import USERS, admin_required

admin = Blueprint("admin", __name__)


@admin.route("")
@admin_required
def dashboard():
    return render_template("page.html", title="Administration", body="The portal's settings.", links=["/admin/users", "/account"])


@admin.route("/users")
@admin_required
def users():
    return render_template("page.html", title="Users", body=", ".join(sorted(USERS)), links=["/admin"])


@admin.route("/audit")
@admin_required
def audit():
    # Linked from nowhere: reached only when a person approves it from the map.
    return render_template("page.html", title="Audit log", body="Nothing changed today.", links=["/admin"])


@admin.route("/api/users")
@admin_required
def users_api():
    return jsonify(sorted(USERS))
