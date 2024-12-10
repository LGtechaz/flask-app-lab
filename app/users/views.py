from . import bp
from flask import render_template, redirect, request, url_for, make_response, session, flash
from datetime import timedelta

VALID_USERNAME = "user"
VALID_PASSWORD = "pass"

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("login")
        password = request.form.get("password")
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Success: session added successfully.", "success")
            return redirect(url_for("user_name.profile"))
        else:
            flash("Incorrect data! Please try again.", "danger")
            return redirect(url_for("user_name.login"))
            
    return render_template("login.html")

@bp.route('/profile')
def profile():
    return render_template("profile.html")