from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ContactTopicForm
from ..models import ContactTopic

contact_topics_bp = Blueprint("contact_topics", __name__, url_prefix="/contact-topics")

PER_PAGE = 10


def _slug_taken(slug: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(ContactTopic.id).filter_by(slug=slug)
    if exclude_id is not None:
        stmt = stmt.where(ContactTopic.id != exclude_id)
    return db.session.scalar(stmt) is not None


def _label_taken(label: str, exclude_id: int | None = None) -> bool:
    if not label:
        return False
    stmt = db.select(ContactTopic.id).filter_by(form_label=label)
    if exclude_id is not None:
        stmt = stmt.where(ContactTopic.id != exclude_id)
    return db.session.scalar(stmt) is not None


def _apply_form(topic: ContactTopic, form: ContactTopicForm) -> None:
    topic.name = form.name.data.strip()
    topic.slug = form.slug.data.strip().lower()
    topic.form_label = (form.form_label.data or "").strip() or None
    topic.sort_order = form.sort_order.data or 0
    topic.is_active = form.is_active.data


@contact_topics_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(ContactTopic)
    if q:
        stmt = stmt.where(ContactTopic.name.ilike(f"%{q}%"))

    pagination = db.paginate(
        stmt.order_by(ContactTopic.sort_order.asc(), ContactTopic.name.asc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "contact_topics/index.html", pagination=pagination, topics=pagination.items, q=q
    )


@contact_topics_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ContactTopicForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        label = (form.form_label.data or "").strip()
        if _slug_taken(slug):
            form.slug.errors.append("That slug is already in use.")
        elif label and _label_taken(label):
            form.form_label.errors.append("That form label is already in use.")
        else:
            topic = ContactTopic()
            _apply_form(topic, form)
            db.session.add(topic)
            db.session.commit()
            flash(f"Contact topic “{topic.name}” created.", "success")
            return redirect(url_for("contact_topics.index"))

    return render_template("contact_topics/form.html", form=form, topic=None)


@contact_topics_bp.route("/<int:topic_id>/edit", methods=["GET", "POST"])
@login_required
def edit(topic_id):
    topic = db.session.get(ContactTopic, topic_id) or abort(404)
    form = ContactTopicForm(obj=topic)

    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        label = (form.form_label.data or "").strip()
        if _slug_taken(slug, exclude_id=topic.id):
            form.slug.errors.append("That slug is already in use.")
        elif label and _label_taken(label, exclude_id=topic.id):
            form.form_label.errors.append("That form label is already in use.")
        else:
            _apply_form(topic, form)
            db.session.commit()
            flash(f"Contact topic “{topic.name}” updated.", "success")
            return redirect(url_for("contact_topics.index"))

    return render_template("contact_topics/form.html", form=form, topic=topic)


@contact_topics_bp.route("/<int:topic_id>/toggle", methods=["POST"])
@login_required
def toggle(topic_id):
    topic = db.session.get(ContactTopic, topic_id) or abort(404)
    topic.is_active = not topic.is_active
    db.session.commit()
    flash(f"“{topic.name}” {'activated' if topic.is_active else 'deactivated'}.", "success")
    return redirect(request.referrer or url_for("contact_topics.index"))


@contact_topics_bp.route("/<int:topic_id>/delete", methods=["POST"])
@login_required
def delete(topic_id):
    topic = db.session.get(ContactTopic, topic_id) or abort(404)
    name = topic.name
    # ON DELETE SET NULL on contact_requests.topic_id — existing enquiries keep
    # their topic_label snapshot and just lose the live link, so no guard needed.
    db.session.delete(topic)
    db.session.commit()
    flash(f"Contact topic “{name}” deleted.", "success")
    return redirect(url_for("contact_topics.index"))
