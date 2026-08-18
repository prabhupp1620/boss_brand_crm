from datetime import datetime
from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..forms import LoginForm
from ..models import User

auth_bp = Blueprint("auth", __name__)


def _safe_next(target: str | None) -> str:
    """Only allow same-site relative redirects after login."""
    if not target:
        return url_for("dashboard.index")
    parsed = urlparse(target)
    if parsed.netloc or parsed.scheme:
        return url_for("dashboard.index")
    return target


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password.", "error")
        elif not user.is_active:
            flash("This account has been deactivated. Contact an administrator.", "error")
        else:
            login_user(user, remember=form.remember.data)
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            flash(f"Welcome back, {user.name.split()[0]}!", "success")
            return redirect(_safe_next(request.args.get("next")))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))
