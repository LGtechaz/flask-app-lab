from flask import request, redirect, url_for, render_template, abort
from . import app
from app.users.routes import users_bp

app.register_blueprint(users_bp)

@app.route('/')
def main():
    return render_template("base.html")

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

#users

@app.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)

@app.route('/resume')
def resume():
    return render_template("resume.html")

@app.route('/base')
def base():
    return render_template("base.html")

@app.route("/admin")
def admin():
    to_url = url_for("greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@app.route("/andrii")
def andrii():
    to_url = url_for("greetings", name="andrii", age=19, _external=True)     # "http://localhost:8080/hi/andrii?age=19"
    print(to_url)
    return redirect(to_url)
