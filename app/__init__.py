import os
from datetime import datetime

from flask import Flask, render_template, send_from_directory

from .cli import register_cli
from .config import Config
from .extensions import csrf, db, login_manager, migrate
from .storage import media_url


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .blueprints.auth import auth_bp
    from .blueprints.branding import branding_bp
    from .blueprints.clients import clients_bp
    from .blueprints.collections import collections_bp
    from .blueprints.colours import colours_bp
    from .blueprints.contact_topics import contact_topics_bp
    from .blueprints.contacts import contacts_bp
    from .blueprints.dashboard import dashboard_bp
    from .blueprints.leads import leads_bp
    from .blueprints.products import products_bp
    from .blueprints.profile import profile_bp
    from .blueprints.sizes import sizes_bp
    from .blueprints.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(colours_bp)
    app.register_blueprint(sizes_bp)
    app.register_blueprint(leads_bp)
    app.register_blueprint(branding_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(contact_topics_bp)
    app.register_blueprint(clients_bp)

    register_cli(app)

    @app.route("/uploads/<subdir>/<filename>")
    def uploaded_file(subdir, filename):
        # Local-storage backend only — in production (STORAGE_BACKEND=s3),
        # image URLs point straight at the bucket and never hit this route.
        folder = os.path.join(app.config["UPLOAD_FOLDER"], subdir)
        return send_from_directory(folder, filename)

    @app.context_processor
    def inject_globals():
        # media_url resolves stored image paths against the active storage
        # backend, so templates never hard-code the bucket's origin.
        return {"now": datetime.utcnow(), "app_name": "Boss Brand", "media_url": media_url}

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app
