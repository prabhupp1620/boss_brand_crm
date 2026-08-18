from datetime import datetime, timedelta

from flask import Blueprint, render_template
from flask_login import login_required

from ..extensions import db
from ..models import User

dashboard_bp = Blueprint("dashboard", __name__)


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

    # Placeholder tiles until the B2B modules (leads, orders, companies) land.
    stats = [
        {
            "label": "Admin users",
            "value": total_users,
            "delta": f"+{new_this_week} this week",
            "trend": "up",
            "icon": "users",
            "tone": "indigo",
        },
        {
            "label": "Active accounts",
            "value": active_users,
            "delta": f"{total_users - active_users} disabled",
            "trend": "flat",
            "icon": "shield",
            "tone": "emerald",
        },
        {
            "label": "Leads",
            "value": "—",
            "delta": "module coming soon",
            "trend": "flat",
            "icon": "target",
            "tone": "amber",
        },
        {
            "label": "Orders",
            "value": "—",
            "delta": "module coming soon",
            "trend": "flat",
            "icon": "cart",
            "tone": "rose",
        },
    ]

    return render_template(
        "dashboard/index.html",
        stats=stats,
        recent_users=recent_users,
        active_users=active_users,
        total_users=total_users,
    )
