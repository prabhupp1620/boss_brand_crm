from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import PasswordForm, ProfileForm
from ..models import User

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Two forms post to the same URL — prefixes keep their fields (and their
    # submit buttons) from being read as each other's input.
    profile_form = ProfileForm(obj=current_user, prefix="profile")
    password_form = PasswordForm(prefix="password")

    if profile_form.submit.data and profile_form.validate_on_submit():
        email = profile_form.email.data.strip().lower()
        clash = db.session.scalar(
            db.select(User.id).filter_by(email=email).where(User.id != current_user.id)
        )
        if clash:
            profile_form.email.errors.append("That email is already registered.")
        else:
            current_user.name = profile_form.name.data.strip()
            current_user.email = email
            current_user.phone = (profile_form.phone.data or "").strip() or None
            db.session.commit()
            flash("Profile updated.", "success")
            return redirect(url_for("profile.index"))

    if password_form.submit.data and password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            password_form.current_password.errors.append("That is not your current password.")
        else:
            current_user.set_password(password_form.password.data)
            db.session.commit()
            flash("Password changed.", "success")
            return redirect(url_for("profile.index"))

    return render_template(
        "profile/index.html", profile_form=profile_form, password_form=password_form
    )
