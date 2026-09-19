from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..forms import ColourForm
from ..models import Colour

colours_bp = Blueprint("colours", __name__, url_prefix="/colours")

PER_PAGE = 10


def _name_taken(name: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(Colour.id).filter_by(name=name)
    if exclude_id is not None:
        stmt = stmt.where(Colour.id != exclude_id)
    return db.session.scalar(stmt) is not None


@colours_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(Colour)
    if q:
        stmt = stmt.where(Colour.name.ilike(f"%{q}%"))

    pagination = db.paginate(
        stmt.order_by(Colour.sort_order.asc(), Colour.name.asc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "colours/index.html", pagination=pagination, colours=pagination.items, q=q
    )


@colours_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ColourForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        if _name_taken(name):
            form.name.errors.append("That colour name already exists.")
        else:
            colour = Colour(
                name=name,
                hex=form.hex.data.strip().upper(),
                sort_order=form.sort_order.data or 0,
                is_active=form.is_active.data,
            )
            db.session.add(colour)
            db.session.commit()
            flash(f"Colour “{colour.name}” created.", "success")
            return redirect(url_for("colours.index"))

    return render_template("colours/form.html", form=form, colour=None)


@colours_bp.route("/<int:colour_id>/edit", methods=["GET", "POST"])
@login_required
def edit(colour_id):
    colour = db.session.get(Colour, colour_id) or abort(404)
    form = ColourForm(obj=colour)

    if form.validate_on_submit():
        name = form.name.data.strip()
        if _name_taken(name, exclude_id=colour.id):
            form.name.errors.append("That colour name already exists.")
        else:
            colour.name = name
            colour.hex = form.hex.data.strip().upper()
            colour.sort_order = form.sort_order.data or 0
            colour.is_active = form.is_active.data
            db.session.commit()
            flash(f"Colour “{colour.name}” updated.", "success")
            return redirect(url_for("colours.index"))

    return render_template("colours/form.html", form=form, colour=colour)


@colours_bp.route("/<int:colour_id>/toggle", methods=["POST"])
@login_required
def toggle(colour_id):
    colour = db.session.get(Colour, colour_id) or abort(404)
    colour.is_active = not colour.is_active
    db.session.commit()
    flash(f"“{colour.name}” {'activated' if colour.is_active else 'deactivated'}.", "success")
    return redirect(request.referrer or url_for("colours.index"))


@colours_bp.route("/<int:colour_id>/delete", methods=["POST"])
@login_required
def delete(colour_id):
    colour = db.session.get(Colour, colour_id) or abort(404)
    name = colour.name
    try:
        db.session.delete(colour)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete “{name}” — it is still used by one or more products.", "error")
        return redirect(url_for("colours.index"))

    flash(f"Colour “{name}” deleted.", "success")
    return redirect(url_for("colours.index"))
