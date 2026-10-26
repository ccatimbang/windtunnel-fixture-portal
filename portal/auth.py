from functools import wraps
from urllib.parse import urlsplit

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

auth = Blueprint("auth", __name__)

# The fixture's three accounts: user name, password, and role.
USERS = {"admin": ("adminpass", "admin"), "manager": ("managerpass", "manager"), "member": ("memberpass", "member")}
RANKS = {"member": 1, "manager": 2, "admin": 3}


def current_role() -> str | None:
    return session.get("role")


def login_required(view):
    @wraps(view)
    def guarded(*args, **kwargs):
        if current_role() is None:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return guarded


def at_least(role: str):
    def decorator(view):
        @wraps(view)
        def guarded(*args, **kwargs):
            if current_role() is None:
                return redirect(url_for("auth.login", next=request.path))
            if RANKS[current_role()] < RANKS[role]:
                abort(403)
            return view(*args, **kwargs)
        return guarded
    return decorator


manager_required = at_least("manager")
admin_required = at_least("admin")


@auth.route("/login", methods=["GET"])
def login():
    return render_template("login.html", next=request.args.get("next", "/account"), error="")


@auth.route("/login", methods=["POST"])
def sign_in():
    username, password = request.form.get("username", ""), request.form.get("password", "")
    target = request.form.get("next") or "/account"
    # Only a path of this site: a browser reads /\host, like //host, as another site.
    parts = urlsplit(target)
    if not target.startswith("/") or target.startswith("//") or "\\" in target or parts.scheme or parts.netloc:
        target = "/account"
    if USERS.get(username, ("", ""))[0] != password or not password:
        return render_template("login.html", next=target, error="That user name and password do not match."), 401
    session.clear()
    session["user"], session["role"] = username, USERS[username][1]
    return redirect(target)


@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("public.index"))
