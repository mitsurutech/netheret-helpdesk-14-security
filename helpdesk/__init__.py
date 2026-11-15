"""The Netheret help desk web app.

create_app() builds the Flask app. Flask looks for a function with this
name when you run `flask --app helpdesk run`.
"""
import os
import secrets

from flask import Flask

from .extensions import db


def create_app():
    app = Flask(__name__)

    # The secret key signs the session cookie, so nobody can change it.
    # On a real server, set the SECRET_KEY environment variable. If it is not
    # set we make a random key each time the app starts: fine on your own
    # computer, but it signs everybody out when the app restarts.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

    # SQLite keeps the whole database in one file. A relative path like this
    # one is put in the app's "instance" folder, which Git ignores.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdesk.db"

    # Tidy the HTML that templates produce: drop the blank lines left by
    # {% ... %} tags.
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # The session cookie: JavaScript cannot read it (HttpOnly, Flask's
    # default) and other sites' forms do not get it (SameSite=Lax). On a real
    # server with HTTPS, set SESSION_COOKIE_SECURE=1 so it is only sent over
    # HTTPS.
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE") == "1"

    db.init_app(app)

    from . import security
    security.init_app(app)

    from . import filters
    filters.register(app)

    # Values every template can use without being passed them.
    from .models import ROLE_LABELS
    app.jinja_env.globals["role_labels"] = ROLE_LABELS

    # Each part of the app is a blueprint: a group of pages in its own file.
    from . import articles, auth, customer, jobs, main, reports, settings, tickets
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(tickets.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(articles.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(settings.bp)

    # Make any tables that do not exist yet. Importing models first tells
    # SQLAlchemy which tables there are.
    from . import models  # noqa: F401
    with app.app_context():
        db.create_all()

    return app
