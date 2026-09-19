from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..forms import BrandingMethodForm
from ..models import BrandingMethod

branding_bp = Blueprint("branding", __name__, url_prefix="/branding-methods")

PER_PAGE = 10


def _slug_taken(slug: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(BrandingMethod.id).filter_by(slug=slug)
    if exclude_id is not None:
        stmt = stmt.where(BrandingMethod.id != exclude_id)
    return db.session.scalar(stmt) is not None


def _label_taken(label: str, exclude_id: int | None = None) -> bool:
    if not label:
        return False
    stmt = db.select(BrandingMethod.id).filter_by(form_label=label)
    if exclude_id is not None:
        stmt = stmt.where(BrandingMethod.id != exclude_id)
    return db.session.scalar(stmt) is not None


def _apply_form(method: BrandingMethod, form: BrandingMethodForm) -> None:
    method.name = form.name.data.strip()
    method.slug = form.slug.data.strip().lower()
    method.form_label = (form.form_label.data or "").strip() or None
    method.sort_order = form.sort_order.data or 0
    method.is_active = form.is_active.data


@branding_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(BrandingMethod)
    if q:
        stmt = stmt.where(BrandingMethod.name.ilike(f"%{q}%"))

    pagination = db.paginate(
        stmt.order_by(BrandingMethod.sort_order.asc(), BrandingMethod.name.asc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "branding/index.html", pagination=pagination, methods=pagination.items, q=q
    )


@branding_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = BrandingMethodForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        label = (form.form_label.data or "").strip()
        if _slug_taken(slug):
            form.slug.errors.append("That slug is already in use.")
        elif label and _label_taken(label):
            form.form_label.errors.append("That form label is already in use.")
        else:
            method = BrandingMethod()
            _apply_form(method, form)
            db.session.add(method)
            db.session.commit()
            flash(f"Branding method “{method.name}” created.", "success")
            return redirect(url_for("branding.index"))

    return render_template("branding/form.html", form=form, method=None)


@branding_bp.route("/<int:method_id>/edit", methods=["GET", "POST"])
@login_required
def edit(method_id):
    method = db.session.get(BrandingMethod, method_id) or abort(404)
    form = BrandingMethodForm(obj=method)

    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        label = (form.form_label.data or "").strip()
        if _slug_taken(slug, exclude_id=method.id):
            form.slug.errors.append("That slug is already in use.")
        elif label and _label_taken(label, exclude_id=method.id):
            form.form_label.errors.append("That form label is already in use.")
        else:
            _apply_form(method, form)
            db.session.commit()
            flash(f"Branding method “{method.name}” updated.", "success")
            return redirect(url_for("branding.index"))

    return render_template("branding/form.html", form=form, method=method)


@branding_bp.route("/<int:method_id>/toggle", methods=["POST"])
@login_required
def toggle(method_id):
    method = db.session.get(BrandingMethod, method_id) or abort(404)
    method.is_active = not method.is_active
    db.session.commit()
    flash(f"“{method.name}” {'activated' if method.is_active else 'deactivated'}.", "success")
    return redirect(request.referrer or url_for("branding.index"))


@branding_bp.route("/<int:method_id>/delete", methods=["POST"])
@login_required
def delete(method_id):
    method = db.session.get(BrandingMethod, method_id) or abort(404)
    name = method.name
    try:
        db.session.delete(method)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete “{name}” — it is still referenced by one or more leads.", "error")
        return redirect(url_for("branding.index"))

    flash(f"Branding method “{name}” deleted.", "success")
    return redirect(url_for("branding.index"))
