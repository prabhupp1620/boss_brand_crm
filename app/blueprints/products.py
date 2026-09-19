from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import (
    ProductForm,
    ProductImageForm,
    ProductPriceTierForm,
    ProductVariantForm,
)
from ..models import (
    Collection,
    Colour,
    Product,
    ProductImage,
    ProductPriceTier,
    ProductVariant,
    Size,
)
from ..uploads import delete_upload, save_image

products_bp = Blueprint("products", __name__, url_prefix="/products")

PER_PAGE = 10


def _collection_choices():
    collections = db.session.execute(
        db.select(Collection).order_by(Collection.name.asc())
    ).scalars().all()
    return [(c.id, c.name) for c in collections]


def _size_choices():
    sizes = db.session.execute(db.select(Size).order_by(Size.sort_order.asc())).scalars().all()
    return [(s.id, s.label) for s in sizes]


def _colour_choices():
    colours = db.session.execute(
        db.select(Colour).order_by(Colour.sort_order.asc())
    ).scalars().all()
    return [(c.id, c.name) for c in colours]


def _variant_ref_choices():
    return [(0, "— none —")] + _size_choices(), [(0, "— none —")] + _colour_choices()


def _populate_choices(form: ProductForm) -> None:
    form.collection_id.choices = _collection_choices()
    form.size_ids.choices = _size_choices()
    form.colour_ids.choices = _colour_choices()


def _slug_taken(slug: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(Product.id).filter_by(slug=slug)
    if exclude_id is not None:
        stmt = stmt.where(Product.id != exclude_id)
    return db.session.scalar(stmt) is not None


def _apply_form(product: Product, form: ProductForm) -> None:
    product.name = form.name.data.strip()
    product.slug = form.slug.data.strip().lower()
    product.collection_id = form.collection_id.data
    product.garment = form.garment.data
    product.fabric = form.fabric.data.strip()
    product.gsm = (form.gsm.data or "").strip() or None
    product.description = (form.description.data or "").strip() or None
    product.moq = form.moq.data
    product.status = form.status.data
    product.badge = form.badge.data or None
    product.sort_order = form.sort_order.data or 0
    product.seo_title = (form.seo_title.data or "").strip() or None
    product.seo_description = (form.seo_description.data or "").strip() or None
    product.is_active = form.is_active.data
    product.set_sizes(form.size_ids.data)
    product.set_colours(form.colour_ids.data)


def _get_product(product_id: int) -> Product:
    return db.session.get(Product, product_id) or abort(404)


@products_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    collection_id = request.args.get("collection_id", type=int)
    status = (request.args.get("status") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(Product)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(db.or_(Product.name.ilike(like), Product.slug.ilike(like), Product.fabric.ilike(like)))
    if collection_id:
        stmt = stmt.where(Product.collection_id == collection_id)
    if status in Product.STATUSES:
        stmt = stmt.where(Product.status == status)

    pagination = db.paginate(
        stmt.order_by(Product.sort_order.asc(), Product.name.asc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "products/index.html",
        pagination=pagination,
        products=pagination.items,
        collections=db.session.execute(db.select(Collection).order_by(Collection.name.asc())).scalars().all(),
        q=q,
        collection_id=collection_id,
        status=status,
    )


@products_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ProductForm()
    _populate_choices(form)

    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        if _slug_taken(slug):
            form.slug.errors.append("That slug is already in use.")
        else:
            try:
                image_url = (
                    save_image(form.primary_image_file.data, "products")
                    if form.primary_image_file.data else None
                )
            except ValueError as e:
                flash(str(e), "error")
            else:
                product = Product()
                _apply_form(product, form)
                db.session.add(product)
                db.session.commit()
                if image_url:
                    db.session.add(ProductImage(
                        product_id=product.id,
                        url=image_url,
                        alt=(form.primary_image_alt.data or "").strip() or None,
                        sort_order=0,
                    ))
                    db.session.commit()
                flash(f"Product “{product.name}” created. Now add more images, pricing and variants below.", "success")
                return redirect(url_for("products.edit", product_id=product.id))

    return render_template(
        "products/form.html", form=form, product=None,
        image_form=None, tier_form=None, variant_form=None,
    )


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit(product_id):
    product = _get_product(product_id)
    form = ProductForm(obj=product)
    _populate_choices(form)

    if request.method == "GET":
        form.size_ids.data = [s.id for s in product.sizes]
        form.colour_ids.data = [c.id for c in product.colours]

    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        if _slug_taken(slug, exclude_id=product.id):
            form.slug.errors.append("That slug is already in use.")
        else:
            _apply_form(product, form)
            db.session.commit()
            flash(f"Product “{product.name}” updated.", "success")
            return redirect(url_for("products.edit", product_id=product.id))

    size_choices, colour_choices = _variant_ref_choices()
    image_form = ProductImageForm()
    tier_form = ProductPriceTierForm()
    variant_form = ProductVariantForm()
    variant_form.size_id.choices = size_choices
    variant_form.colour_id.choices = colour_choices

    return render_template(
        "products/form.html", form=form, product=product,
        image_form=image_form, tier_form=tier_form, variant_form=variant_form,
    )


@products_bp.route("/<int:product_id>/toggle", methods=["POST"])
@login_required
def toggle(product_id):
    product = _get_product(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    flash(f"“{product.name}” {'activated' if product.is_active else 'deactivated'}.", "success")
    return redirect(request.referrer or url_for("products.index"))


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
@login_required
def delete(product_id):
    product = _get_product(product_id)
    name = product.name
    for image in product.images:
        delete_upload(image.url)
    db.session.delete(product)
    db.session.commit()
    flash(f"Product “{name}” deleted.", "success")
    return redirect(url_for("products.index"))


# --- images -----------------------------------------------------------------

@products_bp.route("/<int:product_id>/images", methods=["POST"])
@login_required
def add_image(product_id):
    product = _get_product(product_id)
    form = ProductImageForm()
    if form.validate_on_submit():
        url = None
        if form.image_file.data:
            try:
                url = save_image(form.image_file.data, "products")
            except ValueError as e:
                flash(str(e), "error")
        elif form.url.data and form.url.data.strip():
            url = form.url.data.strip()
        else:
            flash("Upload a file or provide an image URL.", "error")

        if url:
            next_order = len(product.images)
            db.session.add(ProductImage(
                product_id=product.id,
                url=url,
                alt=(form.alt.data or "").strip() or None,
                sort_order=next_order,
            ))
            db.session.commit()
            flash("Image added.", "success")
    else:
        for field_errors in form.errors.values():
            for err in field_errors:
                flash(err, "error")
    return redirect(url_for("products.edit", product_id=product.id))


@products_bp.route("/<int:product_id>/images/<int:image_id>/delete", methods=["POST"])
@login_required
def delete_image(product_id, image_id):
    product = _get_product(product_id)
    image = db.session.get(ProductImage, image_id)
    if not image or image.product_id != product.id:
        abort(404)
    delete_upload(image.url)
    db.session.delete(image)
    db.session.commit()
    flash("Image removed.", "success")
    return redirect(url_for("products.edit", product_id=product.id))


# --- price tiers --------------------------------------------------------------

@products_bp.route("/<int:product_id>/price-tiers", methods=["POST"])
@login_required
def add_price_tier(product_id):
    product = _get_product(product_id)
    form = ProductPriceTierForm()
    if form.validate_on_submit():
        exists = db.session.scalar(
            db.select(ProductPriceTier.id).filter_by(
                product_id=product.id, min_qty=form.min_qty.data
            )
        )
        if exists:
            flash(f"A price tier for minimum quantity {form.min_qty.data} already exists.", "error")
        else:
            db.session.add(ProductPriceTier(
                product_id=product.id,
                min_qty=form.min_qty.data,
                unit_price=form.unit_price.data,
            ))
            db.session.commit()
            flash("Price tier added.", "success")
    else:
        for field_errors in form.errors.values():
            for err in field_errors:
                flash(err, "error")
    return redirect(url_for("products.edit", product_id=product.id))


@products_bp.route("/<int:product_id>/price-tiers/<int:tier_id>/delete", methods=["POST"])
@login_required
def delete_price_tier(product_id, tier_id):
    product = _get_product(product_id)
    tier = db.session.get(ProductPriceTier, tier_id)
    if not tier or tier.product_id != product.id:
        abort(404)
    db.session.delete(tier)
    db.session.commit()
    flash("Price tier removed.", "success")
    return redirect(url_for("products.edit", product_id=product.id))


# --- variants -----------------------------------------------------------------

@products_bp.route("/<int:product_id>/variants", methods=["POST"])
@login_required
def add_variant(product_id):
    product = _get_product(product_id)
    form = ProductVariantForm()
    size_choices, colour_choices = _variant_ref_choices()
    form.size_id.choices = size_choices
    form.colour_id.choices = colour_choices

    if form.validate_on_submit():
        sku = form.sku.data.strip()
        if db.session.scalar(db.select(ProductVariant.id).filter_by(sku=sku)):
            flash(f"SKU “{sku}” is already in use.", "error")
        else:
            db.session.add(ProductVariant(
                product_id=product.id,
                size_id=form.size_id.data or None,
                colour_id=form.colour_id.data or None,
                sku=sku,
                stock_units=form.stock_units.data,
                hub=(form.hub.data or "").strip() or None,
                status=form.status.data,
            ))
            db.session.commit()
            flash("Variant added.", "success")
    else:
        for field_errors in form.errors.values():
            for err in field_errors:
                flash(err, "error")
    return redirect(url_for("products.edit", product_id=product.id))


@products_bp.route("/<int:product_id>/variants/<int:variant_id>/edit", methods=["POST"])
@login_required
def edit_variant(product_id, variant_id):
    product = _get_product(product_id)
    variant = db.session.get(ProductVariant, variant_id)
    if not variant or variant.product_id != product.id:
        abort(404)

    form = ProductVariantForm()
    size_choices, colour_choices = _variant_ref_choices()
    form.size_id.choices = size_choices
    form.colour_id.choices = colour_choices

    if form.validate_on_submit():
        sku = form.sku.data.strip()
        if db.session.scalar(
            db.select(ProductVariant.id).filter_by(sku=sku).where(ProductVariant.id != variant.id)
        ):
            flash(f"SKU “{sku}” is already in use.", "error")
        else:
            variant.size_id = form.size_id.data or None
            variant.colour_id = form.colour_id.data or None
            variant.sku = sku
            variant.stock_units = form.stock_units.data
            variant.hub = (form.hub.data or "").strip() or None
            variant.status = form.status.data
            db.session.commit()
            flash("Variant updated.", "success")
    else:
        for field_errors in form.errors.values():
            for err in field_errors:
                flash(err, "error")
    return redirect(url_for("products.edit", product_id=product.id))


@products_bp.route("/<int:product_id>/variants/<int:variant_id>/delete", methods=["POST"])
@login_required
def delete_variant(product_id, variant_id):
    product = _get_product(product_id)
    variant = db.session.get(ProductVariant, variant_id)
    if not variant or variant.product_id != product.id:
        abort(404)
    db.session.delete(variant)
    db.session.commit()
    flash("Variant removed.", "success")
    return redirect(url_for("products.edit", product_id=product.id))
