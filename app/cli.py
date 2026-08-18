import click

from .extensions import db


def register_cli(app):
    @app.cli.command("init-db")
    def init_db():
        """Create any missing tables (users, ...)."""
        from .models import User  # noqa: F401 - registers the mapper

        db.create_all()
        click.secho("✓ Tables created / verified.", fg="green")

    @app.cli.command("seed")
    def seed():
        """Create the bootstrap admin from ADMIN_* values in .env."""
        from .models import User

        db.create_all()
        email = app.config["ADMIN_EMAIL"].strip().lower()
        existing = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()

        if existing:
            existing.set_password(app.config["ADMIN_PASSWORD"])
            existing.is_active = True
            db.session.commit()
            click.secho(f"↻ Password reset for existing admin {email}", fg="yellow")
        else:
            user = User(
                name=app.config["ADMIN_NAME"],
                email=email,
                role="admin",
                is_active=True,
            )
            user.set_password(app.config["ADMIN_PASSWORD"])
            db.session.add(user)
            db.session.commit()
            click.secho(f"✓ Admin created: {email}", fg="green")

        click.secho(f"  password: {app.config['ADMIN_PASSWORD']}", fg="cyan")

    @app.shell_context_processor
    def shell_context():
        from .models import User

        return {"db": db, "User": User}
