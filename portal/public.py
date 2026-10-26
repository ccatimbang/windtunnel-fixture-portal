from flask import Blueprint, render_template

public = Blueprint("public", __name__)


@public.route("/")
def index():
    return render_template("page.html", title="Fixture Portal", body="Projects, reports, and their people, in one place.",
                           links=["/about", "/pricing", "/login", "/register"])


@public.route("/about")
def about():
    return render_template("page.html", title="About", body="A portal whose pages are kept for some of its accounts.", links=["/"])


@public.route("/pricing")
def pricing():
    return render_template("page.html", title="Pricing", body="One plan, for every team.", links=["/"])
