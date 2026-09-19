from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..forms import SizeForm
from ..models import Size

sizes_bp = Blueprint("sizes", __name__, url_prefix="/sizes")

PER_PAGE = 10


def _label_taken(label: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(Size.id).filter_by(label=label)
    if exclude_id is not None:
        stmt = stmt.where(Size.id != exclude_id)
    return db.session.scalar(stmt) is not None


@sizes_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(Size)
    if q:
        stmt = stmt.where(Size.label.ilike(f"%{q}%"))

    pagination = db.paginate(
        stmt.order_by(Size.sort_order.asc(), Size.label.asc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template("sizes/index.html", pagination=pagination, sizes=pagination.items, q=q)


@sizes_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = SizeForm()
    if form.validate_on_submit():
        label = form.label.data.strip().upper()
        if _label_taken(label):
            form.label.errors.append("That size label already exists.")
        else:
            size = Size(label=label, sort_order=form.sort_order.data or 0)
            db.session.add(size)
            db.session.commit()
            flash(f"Size “{size.label}” created.", "success")
            return redirect(url_for("sizes.index"))

    return render_template("sizes/form.html", form=form, size=None)


@sizes_bp.route("/<int:size_id>/edit", methods=["GET", "POST"])
@login_required
def edit(size_id):
    size = db.session.get(Size, size_id) or abort(404)
    form = SizeForm(obj=size)

    if form.validate_on_submit():
        label = form.label.data.strip().upper()
        if _label_taken(label, exclude_id=size.id):
            form.label.errors.append("That size label already exists.")
        else:
            size.label = label
            size.sort_order = form.sort_order.data or 0
            db.session.commit()
            flash(f"Size “{size.label}” updated.", "success")
            return redirect(url_for("sizes.index"))

    return render_template("sizes/form.html", form=form, size=size)


@sizes_bp.route("/<int:size_id>/delete", methods=["POST"])
@login_required
def delete(size_id):
    size = db.session.get(Size, size_id) or abort(404)
    label = size.label
    try:
        db.session.delete(size)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete “{label}” — it is still used by one or more products.", "error")
        return redirect(url_for("sizes.index"))

    flash(f"Size “{label}” deleted.", "success")
    return redirect(url_for("sizes.index"))
