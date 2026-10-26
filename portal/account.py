from flask import Blueprint, jsonify, render_template, request, session

from portal.auth import login_required

account = Blueprint("account", __name__)

PROJECTS = {1: "Launch", 2: "Migration"}


@account.route("")
@login_required
def home():
    links = ["/account/orders", "/account/settings", "/account/projects", "/billing/invoices"]
    if session["role"] in ("manager", "admin"):
        links.append("/reports")
    if session["role"] == "admin":
        links.append("/admin")
    return render_template("page.html", title="Your account", body=f"Signed in as {session['user']}.", links=links + ["/logout"])


@account.route("/orders")
@login_required
def orders():
    return render_template("page.html", title="Orders", body="No orders yet.", links=["/account"])


@account.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template("page.html", title="Settings", body="Your name and email.", links=["/account"])


@account.route("/settings", methods=["POST"])
@login_required
def save_settings():
    return jsonify({"saved": bool(request.form)})


@account.route("/projects")
@login_required
def projects():
    return render_template("page.html", title="Projects", body="Your projects.",
                           links=[f"/account/projects/{number}" for number in PROJECTS] + ["/account"])


@account.route("/projects/<int:project_id>")
@login_required
def project(project_id: int):
    return render_template("page.html", title=PROJECTS.get(project_id, "Project"), body="A project.", links=["/account/projects"])


@account.route("/api/me")
@login_required
def me():
    return jsonify({"user": session["user"], "role": session["role"]})
