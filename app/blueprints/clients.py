from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ClientForm
from ..models import Client
from ..uploads import delete_upload, save_image

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")

PER_PAGE = 10


def _slug_taken(slug: str, exclude_id: int | None = None) -> bool:
    stmt = db.select(Client.id).filter_by(slug=slug)
    if exclude_id is not None:
        stmt = stmt.where(Client.id != exclude_id)
    return db.session.scalar(stmt) is not None


def _apply_logo(client: Client, form: ClientForm) -> None:
    """Uploaded file wins, then the remove checkbox, then a pasted path."""
    old_url = client.logo_path

    if form.logo_file.data:
        new_url = save_image(form.logo_file.data, "clients")
        client.logo_path = new_url
        if old_url and old_url != new_url:
            delete_upload(old_url)
    elif form.remove_logo.data:
        client.logo_path = None
        if old_url:
            delete_upload(old_url)
    else:
        client.logo_path = (form.logo_path.data or "").strip() or None


def _apply_form(client: Client, form: ClientForm) -> None:
    client.name = form.name.data.strip()
    client.slug = form.slug.data.strip().lower()
    client.sector = (form.sector.data or "").strip() or None
    _apply_logo(client, form)
    client.permission_granted = 1 if form.permission_granted.data else 0
    client.permission_date = form.permission_date.data
    client.permission_note = (form.permission_note.data or "").strip() or None
    client.sort_order = form.sort_order.data or 0
    client.is_active = 1 if form.is_active.data else 0


@clients_bp.route("/")
@login_required
def index():
    q = (request.args.get("q") or "").strip()
    status = (request.args.get("status") or "").strip()
    permission = (request.args.get("permission") or "").strip()
    page = request.args.get("page", 1, type=int)

    stmt = db.select(Client)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            db.or_(Client.name.ilike(like), Client.slug.ilike(like), Client.sector.ilike(like))
        )
    if status in ("active", "inactive"):
        stmt = stmt.where(Client.is_active == (1 if status == "active" else 0))
    if permission in ("granted", "pending"):
        stmt = stmt.where(Client.permission_granted == (1 if permission == "granted" else 0))

    pagination = db.paginate(
        stmt.order_by(Client.sort_order.asc(), Client.name.asc()),
        page=page, per_page=PER_PAGE, error_out=False,
    )
    return render_template(
        "clients/index.html",
        pagination=pagination,
        clients=pagination.items,
        q=q,
        status=status,
        permission=permission,
    )


@clients_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ClientForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        if _slug_taken(slug):
            form.slug.errors.append("That slug is already in use.")
        else:
            try:
                client = Client()
                _apply_form(client, form)
            except ValueError as e:
                flash(str(e), "error")
            else:
                db.session.add(client)
                db.session.commit()
                flash(f"Client “{client.name}” created.", "success")
                return redirect(url_for("clients.index"))

    return render_template("clients/form.html", form=form, client=None)


@clients_bp.route("/<int:client_id>/edit", methods=["GET", "POST"])
@login_required
def edit(client_id):
    client = db.session.get(Client, client_id) or abort(404)
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        slug = form.slug.data.strip().lower()
        if _slug_taken(slug, exclude_id=client.id):
            form.slug.errors.append("That slug is already in use.")
        else:
            try:
                _apply_form(client, form)
            except ValueError as e:
                flash(str(e), "error")
            else:
                db.session.commit()
                flash(f"Client “{client.name}” updated.", "success")
                return redirect(url_for("clients.index"))

    return render_template("clients/form.html", form=form, client=client)


@clients_bp.route("/<int:client_id>/toggle", methods=["POST"])
@login_required
def toggle(client_id):
    client = db.session.get(Client, client_id) or abort(404)
    client.is_active = 0 if client.is_active else 1
    db.session.commit()
    flash(
        f"“{client.name}” {'activated' if client.is_active else 'deactivated'}.",
        "success",
    )
    return redirect(request.referrer or url_for("clients.index"))


@clients_bp.route("/<int:client_id>/delete", methods=["POST"])
@login_required
def delete(client_id):
    client = db.session.get(Client, client_id) or abort(404)
    name = client.name
    delete_upload(client.logo_path)
    db.session.delete(client)
    db.session.commit()
    flash(f"Client “{name}” deleted.", "success")
    return redirect(url_for("clients.index"))
