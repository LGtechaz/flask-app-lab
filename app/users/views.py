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
            session.permanent = True  # Сесія буде активною тривалий час
            flash("Success: You are now logged in!", "success")
            return redirect(url_for("user_name.profile"))
        else:

            flash("Error: Incorrect username or password!", "danger")
            return redirect(url_for("user_name.login"))
            
    return render_template("login.html")

@bp.route('/profile')
def profile():
    if "username" not in session:
        flash("You must log in first.", "danger")
        return redirect(url_for("user_name.login"))

    return render_template("profile.html", username=session["username"])

@bp.route('/logout')
def logout():
    # Видалення інформації про користувача із сесії
    session.pop("username", None)
    session.pop("is_authenticated", None)  # Опціонально, якщо зберігаєте статус
    flash("You have been logged out.", "success")
    return redirect(url_for("user_name.login"))
