from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = 'super_secret_key'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/archive")
def archive():
    return render_template("archive.html")


@app.route("/news")
def news():
    return render_template("news.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        if os.path.exists("messages.json"):
            with open("messages.json", "r", encoding="utf-8") as f:
                messages = json.load(f)
        else:
            messages = []

        messages.append({"name": name, "message": message})

        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        return render_template("contact.html", success=True)
    return render_template("contact.html")


@app.route("/sitemap")
def sitemap():
    return render_template("sitemap.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/articles/<page>")
def show_article(page):
    return render_template(f"articles/{page}.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        else:
            users = {}

        if username in users:
            return "Пользователь уже существует"
        users[username] = password

        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f)

        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        else:
            users = {}

        if username in users and users[username] == password:
            session["username"] = username
            return redirect("/profile")
        else:
            return "Неверный логин или пароль"

    return render_template("login.html")


@app.route("/profile")
def profile():
    if "username" in session:
        messages = []
        if session["username"] == "admin" and os.path.exists("messages.json"):
            with open("messages.json", "r", encoding="utf-8") as f:
                messages = json.load(f)
        return render_template("profile.html", username=session["username"], messages=messages)
    return redirect("/login")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

