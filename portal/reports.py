from flask import Blueprint, render_template

from portal.auth import manager_required

reports = Blueprint("reports", __name__)


@reports.route("")
@manager_required
def overview():
    return render_template("page.html", title="Reports", body="This quarter at a glance.", links=["/reports/sales", "/account"])


@reports.route("/sales")
@manager_required
def sales():
    return render_template("page.html", title="Sales", body="Sales by month.", links=["/reports"])


@reports.route("/team")
@manager_required
def team():
    # Linked from no page.
    return render_template("page.html", title="Team", body="Who works on what.", links=["/reports"])
