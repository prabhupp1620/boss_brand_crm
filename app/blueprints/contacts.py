import secrets

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ContactRequestForm
from ..models import ContactRequest, ContactTopic

contacts_bp = Blueprint("contacts", __name__, url_prefix="/enquiries")

PER_PAGE = 10


def _generate_reference() -> str:
    for _ in range(20):
        ref = f"ENQ-{secrets.token_hex(3).upper()}"
        if not db.session.scalar(db.select(ContactRequest.id).filter_by(reference=ref)):
            return ref
    raise RuntimeError("Could not generate a unique enquiry reference.")


def _topic_choices():
    topics = db.session.execute(
        db.select(ContactTopic).order_by(ContactTopic.sort_order.asc())
    ).scalars().all()
    return [(0, "— none —")] + [(t.id, t.name) for t in topics]


def _populate_choices(form: ContactRequestForm) -> None:
    form.topic_id.choices = _topic_choices()


def _apply_form(contact: ContactRequest, form: ContactRequestForm) -> None:
    contact.name = form.name.data.strip()
    contact.company = form.company.data.strip()
    contact.email = form.email.data.strip().lower()
    contact.phone = (form.phone.data or "").strip() or None
    contact.message = form.message.data.strip()
    contact.status = form.status.data
    contact.status_note = (form.status_note.data or "").strip() or None
    contact.assigned_to = (form.assigned_to.data or "").strip() or None
    contact.replied_at = form.replied_at.data

    topic_id = form.topic_id.data or None
    contact.topic_id = topic_id
    if topic_id:
        topic = db.session.get(ContactTopic, topic_id)
        contact.topic_label = topic.form_label or topic.name if topic else None
    else:
        contact.topic_label = None


def _get_contact(contact_id: int) -> ContactRequest:
    return db.session.get(ContactRequest, contact_id) or abort(404)


@contacts_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    status = (request.args.get("status") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(ContactRequest)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(db.or_(
            ContactRequest.name.ilike(like),
            ContactRequest.company.ilike(like),
            ContactRequest.email.ilike(like),
            ContactRequest.reference.ilike(like),
        ))
    if status in ContactRequest.STATUSES:
        stmt = stmt.where(ContactRequest.status == status)

    pagination = db.paginate(
        stmt.order_by(ContactRequest.created_at.desc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "contacts/index.html",
        pagination=pagination,
        contacts=pagination.items,
        q=q,
        status=status,
    )


@contacts_bp.route("/<int:contact_id>")
@login_required
def view(contact_id):
    """Read-only summary of everything captured for one enquiry.

    Mirrors leads.view. The edit screen only exposes the fields staff may
    change; everything the visitor actually sent — message, intent, referrer,
    UTM tags, IP, user agent — was previously not visible anywhere in the CRM.
    """
    contact = _get_contact(contact_id)
    return render_template("contacts/view.html", contact=contact)


@contacts_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ContactRequestForm()
    _populate_choices(form)
    if not form.status.data:
        form.status.data = "new"

    if form.validate_on_submit():
        contact = ContactRequest(reference=_generate_reference())
        _apply_form(contact, form)
        db.session.add(contact)
        db.session.commit()
        flash(f"Enquiry “{contact.reference}” created.", "success")
        return redirect(url_for("contacts.index"))

    return render_template("contacts/form.html", form=form, contact=None)


@contacts_bp.route("/<int:contact_id>/edit", methods=["GET", "POST"])
@login_required
def edit(contact_id):
    contact = _get_contact(contact_id)
    form = ContactRequestForm(obj=contact)
    _populate_choices(form)

    if request.method == "GET":
        form.topic_id.data = contact.topic_id or 0

    if form.validate_on_submit():
        _apply_form(contact, form)
        db.session.commit()
        flash(f"Enquiry “{contact.reference}” updated.", "success")
        return redirect(url_for("contacts.edit", contact_id=contact.id))

    return render_template("contacts/form.html", form=form, contact=contact)


@contacts_bp.route("/<int:contact_id>/delete", methods=["POST"])
@login_required
def delete(contact_id):
    contact = _get_contact(contact_id)
    ref = contact.reference
    db.session.delete(contact)
    db.session.commit()
    flash(f"Enquiry “{ref}” deleted.", "success")
    return redirect(url_for("contacts.index"))
