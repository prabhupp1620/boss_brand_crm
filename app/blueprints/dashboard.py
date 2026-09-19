import math
from datetime import datetime, timedelta

from flask import Blueprint, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..models import Collection, Colour, ContactRequest, Product, ProductColour, QuoteRequest, User

dashboard_bp = Blueprint("dashboard", __name__)

# Semantic colour, shared across the Leads/Enquiries donuts so a status that
# means the same thing in both pipelines (e.g. "we responded") reads the same.
STATUS_COLOR_VAR = {
    "new": "--chart-blue",
    "in-review": "--chart-yellow",
    "quoted": "--chart-aqua",
    "replied": "--chart-aqua",
    "won": "--chart-green",
    "closed": "--chart-violet",
    "lost": "--chart-violet",
    "spam": "--chart-red",
}


def _donut_segments(pairs, radius=52):
    """pairs: [(label, count), ...] -> ring segments ready for an SVG stroke-dasharray donut."""
    circumference = 2 * math.pi * radius
    total = sum(count for _, count in pairs)
    segments = []
    running = 0.0
    for label, count in pairs:
        length = (count / total * circumference) if total else 0.0
        segments.append({
            "label": label.replace("-", " ").title(),
            "count": count,
            "pct": round(count / total * 100, 1) if total else 0,
            "color_var": STATUS_COLOR_VAR.get(label, "--chart-blue"),
            "dasharray": f"{length:.2f} {circumference - length:.2f}",
            "dashoffset": f"{-running:.2f}",
        })
        running += length
    return segments, total, circumference


def _bar_rows(pairs):
    """pairs: [(label, count), ...] -> rows with a width % scaled to the largest value."""
    max_count = max((c for _, c in pairs), default=0) or 1
    return [
        {"label": label, "count": count, "pct": round(count / max_count * 100, 1)}
        for label, count in pairs
    ]


@dashboard_bp.route("/")
@login_required
def index():
    total_users = db.session.scalar(db.select(db.func.count(User.id))) or 0
    active_users = (
        db.session.scalar(db.select(db.func.count(User.id)).filter_by(is_active=True)) or 0
    )
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_this_week = (
        db.session.scalar(
            db.select(db.func.count(User.id)).where(User.created_at >= week_ago)
        )
        or 0
    )
    recent_users = db.session.execute(
        db.select(User).order_by(User.created_at.desc()).limit(5)
    ).scalars().all()

    total_collections = db.session.scalar(db.select(db.func.count(Collection.id))) or 0
    total_products = db.session.scalar(db.select(db.func.count(Product.id))) or 0
    total_leads = db.session.scalar(db.select(db.func.count(QuoteRequest.id))) or 0
    total_enquiries = db.session.scalar(db.select(db.func.count(ContactRequest.id))) or 0
    leads_this_week = (
        db.session.scalar(
            db.select(db.func.count(QuoteRequest.id)).where(QuoteRequest.created_at >= week_ago)
        )
        or 0
    )
    enquiries_this_week = (
        db.session.scalar(
            db.select(db.func.count(ContactRequest.id)).where(
                ContactRequest.created_at >= week_ago
            )
        )
        or 0
    )

    stats = [
        {
            "label": "Products",
            "value": total_products,
            "delta": f"across {total_collections} collections",
            "trend": "flat",
            "icon": "package",
            "tone": "indigo",
            "href": url_for("products.index"),
        },
        {
            "label": "Leads",
            "value": total_leads,
            "delta": f"+{leads_this_week} this week",
            "trend": "up" if leads_this_week else "flat",
            "icon": "target",
            "tone": "amber",
            "href": url_for("leads.index"),
        },
        {
            "label": "Enquiries",
            "value": total_enquiries,
            "delta": f"+{enquiries_this_week} this week",
            "trend": "up" if enquiries_this_week else "flat",
            "icon": "inbox",
            "tone": "rose",
            "href": url_for("contacts.index"),
        },
        {
            "label": "Admin users",
            "value": total_users,
            "delta": f"+{new_this_week} this week",
            "trend": "up" if new_this_week else "flat",
            "icon": "users",
            "tone": "emerald",
            "href": url_for("users.index"),
        },
    ]

    # --- Products per collection (bar chart, sequential hue = magnitude) -------
    collection_rows = db.session.execute(
        db.select(Collection.name, db.func.count(Product.id))
        .outerjoin(Product, Product.collection_id == Collection.id)
        .group_by(Collection.id)
        .order_by(Collection.sort_order.asc())
    ).all()
    products_by_collection = _bar_rows(collection_rows)

    # --- Leads / Enquiries by status (donut charts) -----------------------------
    lead_counts = dict(
        db.session.execute(
            db.select(QuoteRequest.status, db.func.count(QuoteRequest.id)).group_by(
                QuoteRequest.status
            )
        ).all()
    )
    lead_pairs = [(s, lead_counts.get(s, 0)) for s in QuoteRequest.STATUSES]
    lead_segments, lead_total, lead_circumference = _donut_segments(lead_pairs)

    contact_counts = dict(
        db.session.execute(
            db.select(ContactRequest.status, db.func.count(ContactRequest.id)).group_by(
                ContactRequest.status
            )
        ).all()
    )
    contact_pairs = [(s, contact_counts.get(s, 0)) for s in ContactRequest.STATUSES]
    contact_segments, contact_total, contact_circumference = _donut_segments(contact_pairs)

    # --- Colours in use across the catalogue (bar chart, colour = the data) ----
    colour_rows = db.session.execute(
        db.select(Colour.name, Colour.hex, db.func.count(ProductColour.product_id))
        .join(ProductColour, ProductColour.colour_id == Colour.id)
        .group_by(Colour.id)
        .order_by(db.func.count(ProductColour.product_id).desc())
        .limit(8)
    ).all()
    max_colour_count = max((c for _, _, c in colour_rows), default=0) or 1
    colours_in_use = [
        {"name": name, "hex": hex_, "count": count, "pct": round(count / max_colour_count * 100, 1)}
        for name, hex_, count in colour_rows
    ]

    return render_template(
        "dashboard/index.html",
        stats=stats,
        recent_users=recent_users,
        active_users=active_users,
        total_users=total_users,
        products_by_collection=products_by_collection,
        lead_segments=lead_segments,
        lead_total=lead_total,
        lead_circumference=lead_circumference,
        contact_segments=contact_segments,
        contact_total=contact_total,
        contact_circumference=contact_circumference,
        colours_in_use=colours_in_use,
    )
