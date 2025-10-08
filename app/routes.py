from flask import render_template, request, redirect, session
import json
import os
from app import app  # если routes.py находится в app/

@app.route("/contact", methods=["GET", "POST"])
def contact():
    success = False
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if os.path.exists("messages.json"):
            with open("messages.json", "r", encoding="utf-8") as f:
                try:
                    messages = json.load(f)
                except json.JSONDecodeError:
                    messages = []
        else:
            messages = []

        messages.append({"name": name, "email": email, "message": message})

        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        success = True

    return render_template("contact.html", success=success)


@app.route("/profile")
def profile():
    if "username" in session:
        username = session["username"]
        messages = []
        if username == "admin" and os.path.exists("messages.json"):
            with open("messages.json", "r", encoding="utf-8") as f:
                try:
                    messages = json.load(f)
                except json.JSONDecodeError:
                    messages = []
        return render_template("profile.html", username=username, messages=messages)
    return redirect("/login")
