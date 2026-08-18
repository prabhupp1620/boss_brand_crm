from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import UserForm
from ..models import User

users_bp = Blueprint("users", __name__, url_prefix="/users")

PER_PAGE = 10


def _email_taken(email: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(User.id).filter_by(email=email)
    if exclude_id is not None:
        stmt = stmt.where(User.id != exclude_id)
    return db.session.scalar(stmt) is not None


@users_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    role = (request.args.get("role") or "").strip()
    status = (request.args.get("status") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(User)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(db.or_(User.name.ilike(like), User.email.ilike(like)))
    if role in User.ROLES:
        stmt = stmt.where(User.role == role)
    if status in ("active", "inactive"):
        stmt = stmt.where(User.is_active.is_(status == "active"))

    pagination = db.paginate(
        stmt.order_by(User.created_at.desc()), page=page, per_page=PER_PAGE, error_out=False
    )
    return render_template(
        "users/index.html",
        pagination=pagination,
        users=pagination.items,
        q=q,
        role=role,
        status=status,
    )


@users_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if _email_taken(email):
            form.email.errors.append("That email is already registered.")
        elif not form.password.data:
            form.password.errors.append("A password is required for a new user.")
        else:
            user = User(
                name=form.name.data.strip(),
                email=email,
                phone=(form.phone.data or "").strip() or None,
                role=form.role.data,
                is_active=form.is_active.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f"User “{user.name}” created.", "success")
            return redirect(url_for("users.index"))

    return render_template("users/form.html", form=form, user=None)


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit(user_id):
    user = db.session.get(User, user_id) or abort(404)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if _email_taken(email, exclude_id=user.id):
            form.email.errors.append("That email is already registered.")
        else:
            user.name = form.name.data.strip()
            user.email = email
            user.phone = (form.phone.data or "").strip() or None
            user.role = form.role.data
            # Never let an admin lock themselves out of their own account.
            user.is_active = True if user.id == current_user.id else form.is_active.data
            if form.password.data:
                user.set_password(form.password.data)
            db.session.commit()
            flash(f"User “{user.name}” updated.", "success")
            return redirect(url_for("users.index"))

    return render_template("users/form.html", form=form, user=user)


@users_bp.route("/<int:user_id>/toggle", methods=["POST"])
@login_required
def toggle(user_id):
    user = db.session.get(User, user_id) or abort(404)
    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "error")
        return redirect(url_for("users.index"))

    user.is_active = not user.is_active
    db.session.commit()
    flash(
        f"“{user.name}” {'activated' if user.is_active else 'deactivated'}.",
        "success",
    )
    return redirect(request.referrer or url_for("users.index"))


@users_bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
def delete(user_id):
    user = db.session.get(User, user_id) or abort(404)
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "error")
        return redirect(url_for("users.index"))

    name = user.name
    db.session.delete(user)
    db.session.commit()
    flash(f"User “{name}” deleted.", "success")
    return redirect(url_for("users.index"))
