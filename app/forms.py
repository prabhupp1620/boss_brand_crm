from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DateField,
    DateTimeField,
    DecimalField,
    IntegerField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    widgets,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
    Regexp,
)

from .models import (
    BADGE_CHOICES,
    CONTACT_STATUS_CHOICES,
    GARMENT_CHOICES,
    QUOTE_STATUS_CHOICES,
    STATUS_CHOICES,
)
from .uploads import ALLOWED_IMAGE_EXTENSIONS

GARMENT_SELECT_CHOICES = [(g, g.replace("-", " ").title()) for g in GARMENT_CHOICES]
STATUS_SELECT_CHOICES = [(s, s.replace("-", " ").title()) for s in STATUS_CHOICES]
BADGE_SELECT_CHOICES = [("", "No badge")] + [(b, b) for b in BADGE_CHOICES]
QUOTE_STATUS_SELECT_CHOICES = [(s, s.replace("-", " ").title()) for s in QUOTE_STATUS_CHOICES]
CONTACT_STATUS_SELECT_CHOICES = [(s, s.replace("-", " ").title()) for s in CONTACT_STATUS_CHOICES]


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    email = StringField(
        "Email address",
        validators=[DataRequired(message="Email is required."), Email(), Length(max=190)],
        render_kw={"placeholder": "you@bossbrand.ai", "autocomplete": "email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")],
        render_kw={"placeholder": "••••••••", "autocomplete": "current-password"},
    )
    remember = BooleanField("Keep me signed in")
    submit = SubmitField("Sign in")


class UserForm(FlaskForm):
    """Create / edit an admin user. Password is optional when editing."""

    name = StringField(
        "Full name",
        validators=[DataRequired(), Length(max=120)],
        render_kw={"placeholder": "Jane Cooper"},
    )
    email = StringField(
        "Email address",
        validators=[DataRequired(), Email(), Length(max=190)],
        render_kw={"placeholder": "jane@bossbrand.ai"},
    )
    phone = StringField(
        "Phone",
        validators=[Optional(), Length(max=30)],
        render_kw={"placeholder": "+91 98765 43210"},
    )
    role = SelectField(
        "Role",
        choices=[("admin", "Admin"), ("manager", "Manager"), ("staff", "Staff")],
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[Optional(), Length(min=8, message="Use at least 8 characters.")],
        render_kw={"autocomplete": "new-password"},
    )
    confirm = PasswordField(
        "Confirm password",
        validators=[EqualTo("password", message="Passwords do not match.")],
        render_kw={"autocomplete": "new-password"},
    )
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save user")


class ProfileForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=190)])
    phone = StringField("Phone", validators=[Optional(), Length(max=30)])
    submit = SubmitField("Update profile")


class PasswordForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    password = PasswordField(
        "New password",
        validators=[DataRequired(), Length(min=8, message="Use at least 8 characters.")],
    )
    confirm = PasswordField(
        "Confirm new password",
        validators=[DataRequired(), EqualTo("password", message="Passwords do not match.")],
    )
    submit = SubmitField("Change password")


# =============================================================================
# Catalog forms
# =============================================================================

SLUG_VALIDATOR = Regexp(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    message="Use lowercase letters, numbers and hyphens only, e.g. corporate-t-shirts.",
)


class CollectionForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=160)],
        render_kw={"placeholder": "Corporate T-Shirts"},
    )
    slug = StringField(
        "Slug", validators=[DataRequired(), Length(max=120), SLUG_VALIDATOR],
        render_kw={"placeholder": "corporate-t-shirts", "data-slug-source": "name"},
    )
    tagline = StringField(
        "Tagline", validators=[DataRequired(), Length(max=255)],
        render_kw={"placeholder": "Everyday essentials for the whole team"},
    )
    image_file = FileField(
        "Upload image", validators=[Optional(), FileAllowed(ALLOWED_IMAGE_EXTENSIONS, "Images only.")]
    )
    image_url = StringField(
        "Or image URL / path", validators=[Optional(), Length(max=512)],
        render_kw={"placeholder": "https://… or /products/…"},
    )
    remove_image = BooleanField("Remove current image")
    cutout_file = FileField(
        "Upload cut-out", validators=[Optional(), FileAllowed(ALLOWED_IMAGE_EXTENSIONS, "Images only.")]
    )
    cutout_url = StringField(
        "Or cut-out URL / path", validators=[Optional(), Length(max=512)],
        render_kw={"placeholder": "https://… or /categories/…"},
    )
    remove_cutout = BooleanField("Remove current cut-out")
    garment = SelectField("Garment", choices=GARMENT_SELECT_CHOICES, validators=[DataRequired()])
    moq = IntegerField(
        "MOQ (Minimum Order Quantity)", validators=[DataRequired(), NumberRange(min=1)], default=50
    )
    starting_price_override = DecimalField(
        "Starting price override", validators=[Optional(), NumberRange(min=0)], places=2
    )
    sku_count_override = IntegerField(
        "SKU (Stock Keeping Unit) count override", validators=[Optional(), NumberRange(min=0)]
    )
    sort_order = IntegerField("Sort order", validators=[Optional(), NumberRange(min=0)], default=0)
    seo_title = StringField("SEO (Search Engine Optimization) title", validators=[Optional(), Length(max=200)])
    seo_description = TextAreaField(
        "SEO (Search Engine Optimization) description", validators=[Optional(), Length(max=400)]
    )
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save collection")


class ColourForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=60)],
        render_kw={"placeholder": "Navy Blue"},
    )
    hex = StringField(
        "Hex code",
        validators=[
            DataRequired(),
            Regexp(r"^#[0-9a-fA-F]{6}$", message="Use a 6-digit hex code, e.g. #1F2A44."),
        ],
        render_kw={"placeholder": "#1F2A44"},
    )
    sort_order = IntegerField("Sort order", validators=[Optional(), NumberRange(min=0)], default=0)
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save colour")


class SizeForm(FlaskForm):
    label = StringField(
        "Label", validators=[DataRequired(), Length(max=20)],
        render_kw={"placeholder": "XL"},
    )
    sort_order = IntegerField("Sort order", validators=[Optional(), NumberRange(min=0)], default=0)
    submit = SubmitField("Save size")


class ProductForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=200)],
        render_kw={"placeholder": "Classic Round-Neck Tee"},
    )
    slug = StringField(
        "Slug", validators=[DataRequired(), Length(max=160), SLUG_VALIDATOR],
        render_kw={"placeholder": "classic-round-neck-tee", "data-slug-source": "name"},
    )
    collection_id = SelectField("Collection", coerce=int, validators=[DataRequired()])
    garment = SelectField("Garment", choices=GARMENT_SELECT_CHOICES, validators=[DataRequired()])
    fabric = StringField(
        "Fabric", validators=[DataRequired(), Length(max=160)],
        render_kw={"placeholder": "180 GSM combed cotton"},
    )
    gsm = StringField(
        "GSM (Grams per Square Meter)", validators=[Optional(), Length(max=40)],
        render_kw={"placeholder": "180"},
    )
    description = TextAreaField("Description", validators=[Optional()])
    moq = IntegerField(
        "MOQ (Minimum Order Quantity)", validators=[DataRequired(), NumberRange(min=1)], default=50
    )
    status = SelectField("Stock status", choices=STATUS_SELECT_CHOICES, validators=[DataRequired()])
    badge = SelectField("Badge", choices=BADGE_SELECT_CHOICES, validators=[Optional()])
    sort_order = IntegerField("Sort order", validators=[Optional(), NumberRange(min=0)], default=0)
    seo_title = StringField("SEO (Search Engine Optimization) title", validators=[Optional(), Length(max=200)])
    seo_description = TextAreaField(
        "SEO (Search Engine Optimization) description", validators=[Optional(), Length(max=400)]
    )
    # Named size_ids/colour_ids (not sizes/colours) so they don't collide with
    # Product.sizes / Product.colours — those are read-only properties, and
    # WTForms' obj= binding always prefers an object attribute over explicit
    # data, which would hand this field Size/Colour objects instead of ids.
    size_ids = MultiCheckboxField("Sizes available", coerce=int)
    colour_ids = MultiCheckboxField("Colours available", coerce=int)
    is_active = BooleanField("Active", default=True)

    # Named primary_image_* (not image/images) so they don't collide with
    # Product.images — a real relationship attribute WTForms' obj= binding
    # would otherwise try to hand this field a list of ProductImage rows.
    # Only used at creation time, to seed the first gallery image; once a
    # product exists, the Images section below manages the gallery directly.
    primary_image_file = FileField(
        "Primary image", validators=[Optional(), FileAllowed(ALLOWED_IMAGE_EXTENSIONS, "Images only.")]
    )
    primary_image_alt = StringField("Alt text", validators=[Optional(), Length(max=255)])

    submit = SubmitField("Save product")


class ProductImageForm(FlaskForm):
    image_file = FileField(
        "Upload image", validators=[Optional(), FileAllowed(ALLOWED_IMAGE_EXTENSIONS, "Images only.")]
    )
    url = StringField(
        "Or image URL / path", validators=[Optional(), Length(max=512)],
        render_kw={"placeholder": "https://… or /products/…"},
    )
    alt = StringField("Alt text", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Add image")


class ProductPriceTierForm(FlaskForm):
    min_qty = IntegerField("Min quantity", validators=[DataRequired(), NumberRange(min=1)])
    unit_price = DecimalField("Unit price", validators=[DataRequired(), NumberRange(min=0)], places=2)
    submit = SubmitField("Add price tier")


class ProductVariantForm(FlaskForm):
    # 0 stands in for "not tied to a specific size/colour" — size_id/colour_id are
    # nullable FKs, but a plain empty <option value=""> breaks WTForms' int coercion.
    size_id = SelectField("Size", coerce=int)
    colour_id = SelectField("Colour", coerce=int)
    sku = StringField("SKU (Stock Keeping Unit)", validators=[DataRequired(), Length(max=64)])
    stock_units = IntegerField("Stock units", validators=[DataRequired(), NumberRange(min=0)], default=0)
    hub = StringField("Hub", validators=[Optional(), Length(max=80)])
    status = SelectField("Status", choices=STATUS_SELECT_CHOICES, validators=[DataRequired()])
    submit = SubmitField("Add variant")


# =============================================================================
# Leads (quote requests) forms
# =============================================================================

class BrandingMethodForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=80)],
        render_kw={"placeholder": "Screen Printing"},
    )
    slug = StringField(
        "Slug", validators=[DataRequired(), Length(max=60), SLUG_VALIDATOR],
        render_kw={"placeholder": "screen-printing", "data-slug-source": "name"},
    )
    form_label = StringField(
        "Form label",
        validators=[Optional(), Length(max=80)],
        render_kw={"placeholder": "Screen Printing"},
    )
    sort_order = IntegerField("Sort order", validators=[Optional(), NumberRange(min=0)], default=0)
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save branding method")


class QuoteRequestForm(FlaskForm):
    """Lead / quote request — contact details plus pipeline fields."""

    name = StringField("Contact name", validators=[DataRequired(), Length(max=160)])
    company = StringField("Company", validators=[DataRequired(), Length(max=200)])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=254)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=40)])
    destination = StringField("Delivery destination", validators=[DataRequired(), Length(max=200)])
    deadline = DateField("Needed by", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])

    status = SelectField("Status", choices=QUOTE_STATUS_SELECT_CHOICES, validators=[DataRequired()])
    status_note = StringField("Status note", validators=[Optional(), Length(max=255)])
    assigned_to = StringField("Assigned to", validators=[Optional(), Length(max=120)])
    quoted_at = DateTimeField("Quoted at", validators=[Optional()], format="%Y-%m-%dT%H:%M")
    quoted_total = DecimalField("Quoted total", validators=[Optional(), NumberRange(min=0)], places=2)

    branding_ids = MultiCheckboxField("Branding methods requested", coerce=int)
    submit = SubmitField("Save lead")


class QuoteRequestLineForm(FlaskForm):
    # 0 = "not linked to a live product" — this is a point-in-time snapshot, so a
    # line can (and often will, once a SKU is renamed/discontinued) outlive its FK.
    product_id = SelectField("Link to product", coerce=int)
    product_slug = StringField(
        "Product slug (snapshot)", validators=[DataRequired(), Length(max=160)],
        render_kw={"placeholder": "classic-round-neck-tee"},
    )
    product_name = StringField("Product name (snapshot)", validators=[Optional(), Length(max=200)])
    colour_name = StringField("Colour", validators=[Optional(), Length(max=60)])
    colour_hex = StringField(
        "Colour hex", validators=[Optional(), Regexp(r"^#[0-9a-fA-F]{6}$", message="e.g. #1F2A44")]
    )
    line_units = IntegerField("Units", validators=[Optional(), NumberRange(min=0)], default=0)
    quoted_unit_price = DecimalField(
        "Quoted unit price", validators=[Optional(), NumberRange(min=0)], places=2
    )
    line_note = StringField("Line note", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Add line")


class QuoteRequestLineSizeForm(FlaskForm):
    size_label = SelectField("Size", validators=[DataRequired()])
    units = IntegerField("Units", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Add size")


# =============================================================================
# Enquiries (contact requests) forms
# =============================================================================

class ContactTopicForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=80)],
        render_kw={"placeholder": "Bulk order enquiry"},
    )
    slug = StringField(
        "Slug", validators=[DataRequired(), Length(max=60), SLUG_VALIDATOR],
        render_kw={"placeholder": "bulk-order", "data-slug-source": "name"},
    )
    form_label = StringField(
        "Form label",
        validators=[Optional(), Length(max=80)],
        render_kw={"placeholder": "Bulk order enquiry"},
    )
    sort_order = IntegerField("Sort order", validators=[Optional(), NumberRange(min=0)], default=0)
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save topic")


class ContactRequestForm(FlaskForm):
    """Enquiry / contact-us submission — contact details plus pipeline fields."""

    name = StringField("Contact name", validators=[DataRequired(), Length(max=160)])
    company = StringField("Company", validators=[DataRequired(), Length(max=200)])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=254)])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    message = TextAreaField("Message", validators=[DataRequired()])
    topic_id = SelectField("Topic", coerce=int)

    status = SelectField("Status", choices=CONTACT_STATUS_SELECT_CHOICES, validators=[DataRequired()])
    status_note = StringField("Status note", validators=[Optional(), Length(max=255)])
    assigned_to = StringField("Assigned to", validators=[Optional(), Length(max=120)])
    replied_at = DateTimeField("Replied at", validators=[Optional()], format="%Y-%m-%dT%H:%M")

    submit = SubmitField("Save enquiry")


class ClientForm(FlaskForm):
    name = StringField(
        "Client name", validators=[DataRequired(), Length(max=160)],
        render_kw={"placeholder": "Acme Industries"},
    )
    slug = StringField(
        "Slug", validators=[DataRequired(), Length(max=80), SLUG_VALIDATOR],
        render_kw={"placeholder": "acme-industries", "data-slug-source": "name"},
    )
    sector = StringField(
        "Sector", validators=[Optional(), Length(max=80)],
        render_kw={"placeholder": "Manufacturing, IT services, Hospitality…"},
    )
    logo_file = FileField(
        "Upload logo", validators=[Optional(), FileAllowed(ALLOWED_IMAGE_EXTENSIONS, "Images only.")]
    )
    logo_path = StringField(
        "Or logo URL / path", validators=[Optional(), Length(max=512)],
        render_kw={"placeholder": "https://… or /clients/…"},
    )
    remove_logo = BooleanField("Remove current logo")

    permission_granted = BooleanField("Permission granted to show this logo publicly")
    permission_date = DateField("Permission date", validators=[Optional()])
    permission_note = StringField(
        "Permission note", validators=[Optional(), Length(max=255)],
        render_kw={"placeholder": "Email approval from Priya, 12 Aug 2026"},
    )

    sort_order = IntegerField("Sort order", validators=[Optional(), NumberRange(min=0, max=65535)], default=0)
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save client")
