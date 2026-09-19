from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(UserMixin, db.Model):
    """Admin-panel user. Website (B2B) customers get their own table later."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30))
    role = db.Column(db.String(30), nullable=False, default="admin")  # admin | manager | staff
    # Shadows UserMixin.is_active on purpose — Flask-Login reads this column.
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    ROLES = ("admin", "manager", "staff")

    # --- password helpers -------------------------------------------------
    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    # --- presentation -----------------------------------------------------
    @property
    def initials(self) -> str:
        parts = [p for p in (self.name or "").split() if p]
        if not parts:
            return (self.email or "?")[0].upper()
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def role_label(self) -> str:
        return (self.role or "").replace("_", " ").title()

    def __repr__(self) -> str:
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =============================================================================
# Catalog: collections, products and their supporting tables.
# =============================================================================

GARMENT_CHOICES = (
    "round-neck", "full-sleeve", "oversized", "polo", "hoodie", "sweatshirt",
    "jacket", "formal-shirt", "cap", "tote", "mug", "bottle", "kit-box",
)
STATUS_CHOICES = ("in-stock", "low", "made-to-order")
BADGE_CHOICES = ("Best seller", "New", "Sold out")


class Collection(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(160), nullable=False)
    tagline = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(512))
    garment = db.Column(db.String(20), nullable=False)
    moq = db.Column(db.Integer, nullable=False, default=50)
    starting_price_override = db.Column(db.Numeric(10, 2))
    sku_count_override = db.Column(db.Integer)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.String(400))
    crm_id = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    products = db.relationship("Product", backref="collection", lazy="dynamic")

    GARMENTS = GARMENT_CHOICES

    @property
    def garment_label(self) -> str:
        return (self.garment or "").replace("-", " ").title()

    def __repr__(self) -> str:
        return f"<Collection {self.slug}>"


class Colour(db.Model):
    __tablename__ = "colours"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    hex = db.Column(db.String(7), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<Colour {self.name}>"


class Size(db.Model):
    __tablename__ = "sizes"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(20), unique=True, nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"<Size {self.label}>"


class ProductSize(db.Model):
    """Join row: which sizes a product is offered in."""

    __tablename__ = "product_sizes"

    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
    size_id = db.Column(db.Integer, db.ForeignKey("sizes.id"), primary_key=True)

    size = db.relationship("Size")


class ProductColour(db.Model):
    """Join row: which colours a product is offered in, in display order."""

    __tablename__ = "product_colours"

    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )
    colour_id = db.Column(db.Integer, db.ForeignKey("colours.id"), primary_key=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    colour = db.relationship("Colour")


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    url = db.Column(db.String(512), nullable=False)
    alt = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ProductPriceTier(db.Model):
    __tablename__ = "product_price_tiers"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    min_qty = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)


class ProductVariant(db.Model):
    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    size_id = db.Column(db.Integer, db.ForeignKey("sizes.id"))
    colour_id = db.Column(db.Integer, db.ForeignKey("colours.id"))
    sku = db.Column(db.String(64), unique=True, nullable=False)
    stock_units = db.Column(db.Integer, nullable=False, default=0)
    hub = db.Column(db.String(80))
    status = db.Column(db.String(20), nullable=False, default="in-stock")
    crm_id = db.Column(db.String(64))
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    size = db.relationship("Size")
    colour = db.relationship("Colour")

    STATUSES = STATUS_CHOICES


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"), nullable=False)
    garment = db.Column(db.String(20), nullable=False)
    fabric = db.Column(db.String(160), nullable=False)
    gsm = db.Column(db.String(40))
    description = db.Column(db.Text)
    moq = db.Column(db.Integer, nullable=False, default=50)
    status = db.Column(db.String(20), nullable=False, default="in-stock")
    badge = db.Column(db.String(20))
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.String(400))
    crm_id = db.Column(db.String(64), unique=True)
    crm_sku = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    images = db.relationship(
        "ProductImage", backref="product", order_by="ProductImage.sort_order",
        cascade="all, delete-orphan",
    )
    price_tiers = db.relationship(
        "ProductPriceTier", backref="product", order_by="ProductPriceTier.min_qty",
        cascade="all, delete-orphan",
    )
    variants = db.relationship(
        "ProductVariant", backref="product", cascade="all, delete-orphan"
    )
    size_links = db.relationship(
        "ProductSize", backref="product", cascade="all, delete-orphan"
    )
    colour_links = db.relationship(
        "ProductColour", backref="product", order_by="ProductColour.sort_order",
        cascade="all, delete-orphan",
    )

    GARMENTS = GARMENT_CHOICES
    STATUSES = STATUS_CHOICES
    BADGES = BADGE_CHOICES

    @property
    def sizes(self):
        return [link.size for link in self.size_links]

    @property
    def colours(self):
        return [link.colour for link in self.colour_links]

    def set_sizes(self, size_ids) -> None:
        # Diff rather than replace-the-whole-list: reassigning size_links wholesale
        # would delete-then-reinsert rows that keep the same (product_id, size_id),
        # and SQLAlchemy issues inserts before deletes in a flush, so that trips a
        # duplicate primary key error whenever a size stays checked across an edit.
        keep_ids = set(size_ids or [])
        existing = {link.size_id: link for link in self.size_links}
        for sid, link in existing.items():
            if sid not in keep_ids:
                self.size_links.remove(link)
        for sid in keep_ids:
            if sid not in existing:
                self.size_links.append(ProductSize(size_id=sid))

    def set_colours(self, colour_ids) -> None:
        colour_ids = list(dict.fromkeys(colour_ids or []))  # de-dupe, keep order
        keep_ids = set(colour_ids)
        existing = {link.colour_id: link for link in self.colour_links}
        for cid, link in list(existing.items()):
            if cid not in keep_ids:
                self.colour_links.remove(link)
        for i, cid in enumerate(colour_ids):
            if cid in existing:
                existing[cid].sort_order = i
            else:
                self.colour_links.append(ProductColour(colour_id=cid, sort_order=i))

    @property
    def garment_label(self) -> str:
        return (self.garment or "").replace("-", " ").title()

    @property
    def status_label(self) -> str:
        return (self.status or "").replace("-", " ").title()

    @property
    def primary_image(self):
        return self.images[0] if self.images else None

    def __repr__(self) -> str:
        return f"<Product {self.slug}>"


# =============================================================================
# Leads: quote requests captured from the site's /quote form.
# =============================================================================

QUOTE_STATUS_CHOICES = ("new", "in-review", "quoted", "won", "lost", "spam")


class BrandingMethod(db.Model):
    __tablename__ = "branding_methods"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    form_label = db.Column(db.String(80), unique=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<BrandingMethod {self.slug}>"


class QuoteRequestBranding(db.Model):
    """Join row: one ticked branding checkbox on a submitted quote."""

    __tablename__ = "quote_request_branding"

    quote_request_id = db.Column(
        db.Integer, db.ForeignKey("quote_requests.id", ondelete="CASCADE"), primary_key=True
    )
    submitted_label = db.Column(db.String(80), primary_key=True)
    branding_method_id = db.Column(db.Integer, db.ForeignKey("branding_methods.id"))

    branding_method = db.relationship("BrandingMethod")


class QuoteRequestLineSize(db.Model):
    __tablename__ = "quote_request_line_sizes"

    id = db.Column(db.Integer, primary_key=True)
    quote_request_line_id = db.Column(
        db.Integer, db.ForeignKey("quote_request_lines.id", ondelete="CASCADE"), nullable=False
    )
    size_id = db.Column(db.Integer, db.ForeignKey("sizes.id"))
    size_label = db.Column(db.String(20), nullable=False)
    units = db.Column(db.Integer, nullable=False)

    size = db.relationship("Size")


class QuoteRequestLine(db.Model):
    """One product + colourway in a quote's basket."""

    __tablename__ = "quote_request_lines"

    id = db.Column(db.Integer, primary_key=True)
    quote_request_id = db.Column(
        db.Integer, db.ForeignKey("quote_requests.id", ondelete="CASCADE"), nullable=False
    )
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="SET NULL"))
    product_slug = db.Column(db.String(160), nullable=False)
    product_name = db.Column(db.String(200))
    colour_name = db.Column(db.String(60))
    colour_hex = db.Column(db.String(7))
    line_units = db.Column(db.Integer, nullable=False, default=0)
    quoted_unit_price = db.Column(db.Numeric(10, 2))
    line_note = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship("Product")
    sizes = db.relationship(
        "QuoteRequestLineSize", backref="line", order_by="QuoteRequestLineSize.id",
        cascade="all, delete-orphan",
    )

    def recompute_units(self) -> None:
        if self.sizes:
            self.line_units = sum(s.units for s in self.sizes)


class QuoteRequest(db.Model):
    """One row per /quote form submission — a lead in the sales pipeline."""

    __tablename__ = "quote_requests"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(160), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date)
    notes = db.Column(db.Text)

    status = db.Column(db.String(20), nullable=False, default="new")
    status_note = db.Column(db.String(255))
    assigned_to = db.Column(db.String(120))
    quoted_at = db.Column(db.DateTime)
    quoted_total = db.Column(db.Numeric(12, 2))

    prefill_product = db.Column(db.String(60))
    prefill_qty = db.Column(db.Integer)
    prefill_branding = db.Column(db.String(60))

    source_page = db.Column(db.String(255))
    referrer = db.Column(db.String(512))
    utm_source = db.Column(db.String(120))
    utm_medium = db.Column(db.String(120))
    utm_campaign = db.Column(db.String(120))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(512))

    total_units = db.Column(db.Integer, nullable=False, default=0)
    crm_id = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    lines = db.relationship(
        "QuoteRequestLine", backref="quote_request", order_by="QuoteRequestLine.sort_order",
        cascade="all, delete-orphan",
    )
    branding_links = db.relationship(
        "QuoteRequestBranding", backref="quote_request", cascade="all, delete-orphan"
    )

    STATUSES = QUOTE_STATUS_CHOICES

    @property
    def branding_labels(self):
        return [link.submitted_label for link in self.branding_links]

    def set_branding(self, branding_method_ids) -> None:
        methods = {
            m.id: m
            for m in db.session.execute(
                db.select(BrandingMethod).where(BrandingMethod.id.in_(branding_method_ids or []))
            ).scalars()
        }
        keep_labels = {m.form_label or m.name for m in methods.values()}
        existing = {link.submitted_label: link for link in self.branding_links}
        for label, link in list(existing.items()):
            if label not in keep_labels:
                self.branding_links.remove(link)
        for mid, method in methods.items():
            label = method.form_label or method.name
            if label not in existing:
                self.branding_links.append(
                    QuoteRequestBranding(submitted_label=label, branding_method_id=mid)
                )

    def recompute_total_units(self) -> None:
        self.total_units = sum(line.line_units for line in self.lines)

    @property
    def status_label(self) -> str:
        return (self.status or "").replace("-", " ").title()

    def __repr__(self) -> str:
        return f"<QuoteRequest {self.reference}>"


# =============================================================================
# Enquiries: general contact-us form submissions.
# =============================================================================

CONTACT_STATUS_CHOICES = ("new", "in-review", "replied", "closed", "spam")


class ContactTopic(db.Model):
    __tablename__ = "contact_topics"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    form_label = db.Column(db.String(80), unique=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<ContactTopic {self.slug}>"


class ContactRequest(db.Model):
    """One row per /contact form submission — a general enquiry."""

    __tablename__ = "contact_requests"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(160), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(40))

    topic_id = db.Column(db.Integer, db.ForeignKey("contact_topics.id", ondelete="SET NULL"))
    topic_label = db.Column(db.String(80))
    intent = db.Column(db.String(60))

    status = db.Column(db.String(20), nullable=False, default="new")
    status_note = db.Column(db.String(255))
    assigned_to = db.Column(db.String(120))
    replied_at = db.Column(db.DateTime)

    source_page = db.Column(db.String(255))
    referrer = db.Column(db.String(512))
    utm_source = db.Column(db.String(120))
    utm_medium = db.Column(db.String(120))
    utm_campaign = db.Column(db.String(120))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(512))

    crm_id = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    topic = db.relationship("ContactTopic")

    STATUSES = CONTACT_STATUS_CHOICES

    @property
    def status_label(self) -> str:
        return (self.status or "").replace("-", " ").title()

    @property
    def topic_display(self) -> str:
        return (self.topic.name if self.topic else self.topic_label) or "—"

    def __repr__(self) -> str:
        return f"<ContactRequest {self.reference}>"
