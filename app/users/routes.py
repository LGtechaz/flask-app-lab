from flask import Blueprint, render_template, request, redirect, url_for

users_bp = Blueprint("users",
                      __name__,
                        url_prefix="/users",
                        template_folder="templates/users"
                        )

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)
