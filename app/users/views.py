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

#@bp.route('/profile')
#def profile():
  #  if "username" not in session:
       # //flash("You must log in first.", "danger")
       # //return redirect(url_for("user_name.login"))
#
 #   //return render_template("profile.html", username=session["username"])

@bp.route('/logout')
def logout():
    # Видалення інформації про користувача із сесії
    session.pop("username", None)
    session.pop("is_authenticated", None)  # Опціонально, якщо зберігаєте статус
    flash("You have been logged out.", "success")
    return redirect(url_for("user_name.login"))

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    # Перевірка автентифікації
    if "username" not in session:
        flash("You must log in first.", "danger")
        return redirect(url_for("user_name.login"))

    response = make_response(render_template(
        "profile.html", 
        username=session["username"], 
        cookies=request.cookies  # Передача cookies у шаблон
    ))

    # Обробка додавання кукі
    if request.method == "POST" and "add_cookie" in request.form:
        key = request.form.get("cookie_key")
        value = request.form.get("cookie_value")
        max_age = request.form.get("cookie_max_age", type=int)  # Час у секундах
        if key and value:
            response.set_cookie(key, value, max_age=max_age)
            flash(f"Cookie '{key}' added successfully!", "success")
        else:
            flash("Key and value are required to add a cookie.", "danger")

    # Обробка видалення кукі за ключем
    elif request.method == "POST" and "delete_cookie" in request.form:
        key = request.form.get("cookie_key")
        if key in request.cookies:
            response.delete_cookie(key)
            flash(f"Cookie '{key}' deleted successfully!", "success")
        else:
            flash(f"Cookie '{key}' does not exist.", "danger")

    # Обробка видалення всіх кукі
    elif request.method == "POST" and "delete_all_cookies" in request.form:
        for cookie_key in request.cookies.keys():
            response.delete_cookie(cookie_key)
        flash("All cookies deleted successfully!", "success")

    return response