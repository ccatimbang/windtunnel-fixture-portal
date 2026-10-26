from flask import Blueprint, render_template

from portal.auth import login_required

billing = Blueprint("billing", __name__)

INVOICES = {101: "October", 102: "November"}


def section(name: str) -> str:
    """The path of one of the account's sections: /billing for billing."""
    return "/" + name


@billing.route(section("billing") + "/invoices")
@login_required
def invoices():
    return render_template("page.html", title="Invoices", body="Your invoices.",
                           links=[f"/billing/invoices/{number}" for number in INVOICES] + ["/account"])


@billing.route(section("billing") + "/invoices/<int:invoice_id>")
@login_required
def invoice(invoice_id: int):
    return render_template("page.html", title=INVOICES.get(invoice_id, "Invoice"), body="An invoice.", links=["/billing/invoices"])
