from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
)


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
