"""Security checks that apply to every page.

CSRF (cross-site request forgery): another website could contain a hidden
form that posts to our app. The browser would send our session cookie with
it, so the app would think the signed-in user had pressed the button.

The fix, written by hand: we keep a random token in the session and put it
in a hidden field in every form we make. A POST without the right token did
not come from one of our pages, so it is refused.
"""
import secrets

from flask import abort, request, session


def csrf_token():
    """The session's CSRF token, made the first time a form needs it."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def check_csrf():
    """Runs before every request and refuses a POST without the right token."""
    if request.method != "POST":
        return
    expected = session.get("csrf_token")
    sent = request.form.get("csrf_token")
    # compare_digest takes the same time whether the first letter or the
    # last is wrong, so timing cannot give the token away.
    if not expected or not sent or not secrets.compare_digest(expected, sent):
        abort(400)


def add_security_headers(response):
    """Headers that tell the browser to be stricter with our pages."""
    # Only run scripts, styles and images from our own site.
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'"
    )
    # Do not let other sites show our pages inside a frame (clickjacking).
    response.headers["X-Frame-Options"] = "DENY"
    # Do not guess file types: a .txt file is never run as a script.
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Do not send our addresses (which contain request ids) to other sites.
    response.headers["Referrer-Policy"] = "same-origin"
    return response


def init_app(app):
    app.before_request(check_csrf)
    app.after_request(add_security_headers)
    # Templates call {{ csrf_token() }} inside every form.
    app.jinja_env.globals["csrf_token"] = csrf_token
