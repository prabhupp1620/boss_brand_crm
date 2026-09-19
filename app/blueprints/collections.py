from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import CollectionForm
from ..models import Collection
from ..uploads import delete_upload, save_image

collections_bp = Blueprint("collections", __name__, url_prefix="/collections")

PER_PAGE = 10


def _slug_taken(slug: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(Collection.id).filter_by(slug=slug)
    if exclude_id is not None:
        stmt = stmt.where(Collection.id != exclude_id)
    return db.session.scalar(stmt) is not None


def _apply_image(collection: Collection, form: CollectionForm) -> None:
    old_url = collection.image_url
    if form.image_file.data:
        new_url = save_image(form.image_file.data, "collections")
        collection.image_url = new_url
        if old_url and old_url != new_url:
            delete_upload(old_url)
    elif form.remove_image.data:
        collection.image_url = None
        if old_url:
            delete_upload(old_url)
    else:
        collection.image_url = (form.image_url.data or "").strip() or None


def _apply_form(collection: Collection, form: CollectionForm) -> None:
    collection.name = form.name.data.strip()
    collection.slug = form.slug.data.strip().lower()
    collection.tagline = form.tagline.data.strip()
    _apply_image(collection, form)
    collection.garment = form.garment.data
    collection.moq = form.moq.data
    collection.starting_price_override = form.starting_price_override.data
    collection.sku_count_override = form.sku_count_override.data
    collection.sort_order = form.sort_order.data or 0
    collection.seo_title = (form.seo_title.data or "").strip() or None
    collection.seo_description = (form.seo_description.data or "").strip() or None
    collection.is_active = form.is_active.data


@collections_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    status = (request.args.get("status") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(Collection)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(db.or_(Collection.name.ilike(like), Collection.slug.ilike(like)))
    if status in ("active", "inactive"):
        stmt = stmt.where(Collection.is_active.is_(status == "active"))

    pagination = db.paginate(
        stmt.order_by(Collection.sort_order.asc(), Collection.name.asc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "collections/index.html",
        pagination=pagination,
        collections=pagination.items,
        q=q,
        status=status,
    )


@collections_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = CollectionForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        if _slug_taken(slug):
            form.slug.errors.append("That slug is already in use.")
        else:
            try:
                collection = Collection()
                _apply_form(collection, form)
            except ValueError as e:
                flash(str(e), "error")
            else:
                db.session.add(collection)
                db.session.commit()
                flash(f"Collection “{collection.name}” created.", "success")
                return redirect(url_for("collections.index"))

    return render_template("collections/form.html", form=form, collection=None)


@collections_bp.route("/<int:collection_id>/edit", methods=["GET", "POST"])
@login_required
def edit(collection_id):
    collection = db.session.get(Collection, collection_id) or abort(404)
    form = CollectionForm(obj=collection)

    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        if _slug_taken(slug, exclude_id=collection.id):
            form.slug.errors.append("That slug is already in use.")
        else:
            try:
                _apply_form(collection, form)
            except ValueError as e:
                flash(str(e), "error")
            else:
                db.session.commit()
                flash(f"Collection “{collection.name}” updated.", "success")
                return redirect(url_for("collections.index"))

    return render_template("collections/form.html", form=form, collection=collection)


@collections_bp.route("/<int:collection_id>/toggle", methods=["POST"])
@login_required
def toggle(collection_id):
    collection = db.session.get(Collection, collection_id) or abort(404)
    collection.is_active = not collection.is_active
    db.session.commit()
    flash(
        f"“{collection.name}” {'activated' if collection.is_active else 'deactivated'}.",
        "success",
    )
    return redirect(request.referrer or url_for("collections.index"))


@collections_bp.route("/<int:collection_id>/delete", methods=["POST"])
@login_required
def delete(collection_id):
    collection = db.session.get(Collection, collection_id) or abort(404)
    if collection.products.count():
        flash(
            f"Cannot delete “{collection.name}” — it still has products assigned to it.",
            "error",
        )
        return redirect(url_for("collections.index"))

    name = collection.name
    delete_upload(collection.image_url)
    db.session.delete(collection)
    db.session.commit()
    flash(f"Collection “{name}” deleted.", "success")
    return redirect(url_for("collections.index"))
