"""Each user's accessibility settings: text size and high contrast.

They are saved on the User row, so they follow the person to any computer
they sign in on. base.html turns them into CSS classes on the <html> tag.
"""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .extensions import db
from .models import TEXT_SIZES

bp = Blueprint("settings", __name__)


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def accessibility():
    if request.method == "POST":
        text_size = request.form.get("text_size")
        if text_size not in TEXT_SIZES:
            flash("Choose one of the text sizes.")
        else:
            g.user.text_size = text_size
            g.user.high_contrast = request.form.get("high_contrast") == "yes"
            db.session.commit()
            flash("Your settings are saved.")
        return redirect(url_for("settings.accessibility"))
    return render_template("settings.html", text_sizes=TEXT_SIZES)
