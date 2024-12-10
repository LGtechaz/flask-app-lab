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

@bp.route('/logout')
def logout():
    session.pop("username", None)
    session.pop("is_authenticated", None) 
    flash("You have been logged out.", "success")
    return redirect(url_for("user_name.login"))

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if "username" not in session:
        flash("You must log in first.", "danger")
        return redirect(url_for("user_name.login"))

    theme = request.cookies.get("theme", "light") 

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_cookie":
            key = request.form.get("cookie_key")
            value = request.form.get("cookie_value")
            max_age = request.form.get("cookie_max_age", type=int) 
            if key and value:
                response = make_response(redirect(url_for("user_name.profile")))
                response.set_cookie(key, value, max_age=max_age)
                flash(f"Cookie '{key}' added successfully!", "success")
                return response
            else:
                flash("Key and value are required to add a cookie.", "danger")
                return redirect(url_for("user_name.profile"))

        elif action == "delete_cookie":
            key = request.form.get("cookie_key")
            if key in request.cookies:
                response = make_response(redirect(url_for("user_name.profile")))
                response.delete_cookie(key)
                flash(f"Cookie '{key}' deleted successfully!", "success")
                return response
            else:
                flash(f"Cookie '{key}' does not exist.", "danger")
                return redirect(url_for("user_name.profile"))

        elif action == "delete_all_cookies":
            response = make_response(redirect(url_for("user_name.profile")))
            for cookie_key in request.cookies.keys():
                response.delete_cookie(cookie_key)
            flash("All cookies deleted successfully!", "success")
            return response

    return render_template("profile.html", username=session["username"], cookies=request.cookies, theme=theme)


@bp.route('/set_theme/<theme>', methods=['GET'])
def set_theme(theme):
    if theme not in ["light", "dark"]:
        flash("Invalid theme selected.", "danger")
        return redirect(url_for("user_name.profile"))

    response = make_response(redirect(url_for("user_name.profile")))
    response.set_cookie("theme", theme, max_age=30 * 24 * 60 * 60)  # Зберігаємо на 30 днів
    flash(f"Theme changed to {theme}.", "success")
    return response

