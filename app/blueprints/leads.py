import secrets

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import (
    QuoteRequestForm,
    QuoteRequestLineForm,
    QuoteRequestLineSizeForm,
)
from ..models import (
    BrandingMethod,
    Product,
    QuoteRequest,
    QuoteRequestLine,
    QuoteRequestLineSize,
    Size,
)

leads_bp = Blueprint("leads", __name__, url_prefix="/leads")

PER_PAGE = 10


def _generate_reference() -> str:
    for _ in range(20):
        ref = f"RFQ-{secrets.token_hex(3).upper()}"
        if not db.session.scalar(db.select(QuoteRequest.id).filter_by(reference=ref)):
            return ref
    raise RuntimeError("Could not generate a unique quote reference.")


def _branding_choices():
    methods = db.session.execute(
        db.select(BrandingMethod).order_by(BrandingMethod.sort_order.asc())
    ).scalars().all()
    return [(m.id, m.name) for m in methods]


def _product_choices():
    products = db.session.execute(db.select(Product).order_by(Product.name.asc())).scalars().all()
    return [(0, "— not linked —")] + [(p.id, f"{p.name} ({p.slug})") for p in products]


def _size_label_choices():
    sizes = db.session.execute(db.select(Size).order_by(Size.sort_order.asc())).scalars().all()
    return [(s.label, s.label) for s in sizes]


def _populate_choices(form: QuoteRequestForm) -> None:
    form.branding_ids.choices = _branding_choices()


def _apply_form(lead: QuoteRequest, form: QuoteRequestForm) -> None:
    lead.name = form.name.data.strip()
    lead.company = form.company.data.strip()
    lead.email = form.email.data.strip().lower()
    lead.phone = form.phone.data.strip()
    lead.destination = form.destination.data.strip()
    lead.deadline = form.deadline.data
    lead.notes = (form.notes.data or "").strip() or None
    lead.status = form.status.data
    lead.status_note = (form.status_note.data or "").strip() or None
    lead.assigned_to = (form.assigned_to.data or "").strip() or None
    lead.quoted_at = form.quoted_at.data
    lead.quoted_total = form.quoted_total.data
    lead.set_branding(form.branding_ids.data)


def _get_lead(lead_id: int) -> QuoteRequest:
    return db.session.get(QuoteRequest, lead_id) or abort(404)


@leads_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    status = (request.args.get("status") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(QuoteRequest)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(db.or_(
            QuoteRequest.name.ilike(like),
            QuoteRequest.company.ilike(like),
            QuoteRequest.email.ilike(like),
            QuoteRequest.reference.ilike(like),
        ))
    if status in QuoteRequest.STATUSES:
        stmt = stmt.where(QuoteRequest.status == status)

    pagination = db.paginate(
        stmt.order_by(QuoteRequest.created_at.desc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "leads/index.html",
        pagination=pagination,
        leads=pagination.items,
        q=q,
        status=status,
    )


@leads_bp.route("/<int:lead_id>")
@login_required
def view(lead_id):
    """Read-only summary of everything captured for one lead."""
    lead = _get_lead(lead_id)
    return render_template("leads/view.html", lead=lead)


@leads_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = QuoteRequestForm()
    _populate_choices(form)
    if not form.status.data:
        form.status.data = "new"

    if form.validate_on_submit():
        lead = QuoteRequest(reference=_generate_reference(), total_units=0)
        _apply_form(lead, form)
        db.session.add(lead)
        db.session.commit()
        flash(f"Lead “{lead.reference}” created. Now add the basket lines below.", "success")
        return redirect(url_for("leads.edit", lead_id=lead.id))

    return render_template(
        "leads/form.html", form=form, lead=None, line_form=None, size_forms={}, product_choices=[]
    )


@leads_bp.route("/<int:lead_id>/edit", methods=["GET", "POST"])
@login_required
def edit(lead_id):
    lead = _get_lead(lead_id)
    form = QuoteRequestForm(obj=lead)
    _populate_choices(form)

    if request.method == "GET":
        form.branding_ids.data = [
            link.branding_method_id for link in lead.branding_links if link.branding_method_id
        ]

    if form.validate_on_submit():
        _apply_form(lead, form)
        db.session.commit()
        flash(f"Lead “{lead.reference}” updated.", "success")
        return redirect(url_for("leads.edit", lead_id=lead.id))

    line_form = QuoteRequestLineForm()
    line_form.product_id.choices = _product_choices()

    size_choices = _size_label_choices()
    size_forms = {}
    for line in lead.lines:
        sf = QuoteRequestLineSizeForm()
        sf.size_label.choices = size_choices
        size_forms[line.id] = sf

    return render_template(
        "leads/form.html",
        form=form, lead=lead, line_form=line_form, size_forms=size_forms,
        product_choices=_product_choices(),
    )


@leads_bp.route("/<int:lead_id>/delete", methods=["POST"])
@login_required
def delete(lead_id):
    lead = _get_lead(lead_id)
    ref = lead.reference
    db.session.delete(lead)
    db.session.commit()
    flash(f"Lead “{ref}” deleted.", "success")
    return redirect(url_for("leads.index"))


# --- basket lines -------------------------------------------------------------

@leads_bp.route("/<int:lead_id>/lines", methods=["POST"])
@login_required
def add_line(lead_id):
    lead = _get_lead(lead_id)
    form = QuoteRequestLineForm()
    form.product_id.choices = _product_choices()

    if form.validate_on_submit():
        next_order = len(lead.lines)
        line = QuoteRequestLine(
            quote_request_id=lead.id,
            product_id=(form.product_id.data or None) or None,
            product_slug=form.product_slug.data.strip(),
            product_name=(form.product_name.data or "").strip() or None,
            colour_name=(form.colour_name.data or "").strip() or None,
            colour_hex=(form.colour_hex.data or "").strip().upper() or None,
            line_units=form.line_units.data or 0,
            quoted_unit_price=form.quoted_unit_price.data,
            line_note=(form.line_note.data or "").strip() or None,
            sort_order=next_order,
        )
        db.session.add(line)
        db.session.flush()
        lead.recompute_total_units()
        db.session.commit()
        flash("Basket line added.", "success")
    else:
        for field_errors in form.errors.values():
            for err in field_errors:
                flash(err, "error")
    return redirect(url_for("leads.edit", lead_id=lead.id))


@leads_bp.route("/<int:lead_id>/lines/<int:line_id>/delete", methods=["POST"])
@login_required
def delete_line(lead_id, line_id):
    lead = _get_lead(lead_id)
    line = db.session.get(QuoteRequestLine, line_id)
    if not line or line.quote_request_id != lead.id:
        abort(404)
    db.session.delete(line)
    db.session.flush()
    lead.recompute_total_units()
    db.session.commit()
    flash("Basket line removed.", "success")
    return redirect(url_for("leads.edit", lead_id=lead.id))


# --- size run per line ---------------------------------------------------------

@leads_bp.route("/<int:lead_id>/lines/<int:line_id>/sizes", methods=["POST"])
@login_required
def add_line_size(lead_id, line_id):
    lead = _get_lead(lead_id)
    line = db.session.get(QuoteRequestLine, line_id)
    if not line or line.quote_request_id != lead.id:
        abort(404)

    form = QuoteRequestLineSizeForm()
    form.size_label.choices = _size_label_choices()

    if form.validate_on_submit():
        label = form.size_label.data
        if db.session.scalar(
            db.select(QuoteRequestLineSize.id).filter_by(
                quote_request_line_id=line.id, size_label=label
            )
        ):
            flash(f"Size “{label}” is already on this line.", "error")
        else:
            size_id = db.session.scalar(db.select(Size.id).filter_by(label=label))
            db.session.add(QuoteRequestLineSize(
                quote_request_line_id=line.id,
                size_id=size_id,
                size_label=label,
                units=form.units.data,
            ))
            db.session.flush()
            line.recompute_units()
            lead.recompute_total_units()
            db.session.commit()
            flash("Size added.", "success")
    else:
        for field_errors in form.errors.values():
            for err in field_errors:
                flash(err, "error")
    return redirect(url_for("leads.edit", lead_id=lead.id))


@leads_bp.route("/<int:lead_id>/lines/<int:line_id>/sizes/<int:size_row_id>/delete", methods=["POST"])
@login_required
def delete_line_size(lead_id, line_id, size_row_id):
    lead = _get_lead(lead_id)
    line = db.session.get(QuoteRequestLine, line_id)
    if not line or line.quote_request_id != lead.id:
        abort(404)
    size_row = db.session.get(QuoteRequestLineSize, size_row_id)
    if not size_row or size_row.quote_request_line_id != line.id:
        abort(404)

    db.session.delete(size_row)
    db.session.flush()
    line.recompute_units()
    lead.recompute_total_units()
    db.session.commit()
    flash("Size removed.", "success")
    return redirect(url_for("leads.edit", lead_id=lead.id))
