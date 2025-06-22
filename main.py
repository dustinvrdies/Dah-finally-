import os
import importlib
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from wallet import get_wallet

app = Flask(__name__)
app.secret_key = "dah_secret_key"

PLUGINS_FOLDER = "plugins"
PLUGINS = {}

if os.path.exists(PLUGINS_FOLDER):
    for file in os.listdir(PLUGINS_FOLDER):
        if file.endswith(".py"):
            module_name = file[:-3]
            module = importlib.import_module(f"{PLUGINS_FOLDER}.{module_name}")
            PLUGINS[module_name] = module

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["logged_in"] = True
        return redirect("/home")
    return render_template("login.html")

@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("home.html")

@app.route("/bots")
def bots():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("bots.html")

@app.route("/wallet")
def wallet():
    if not session.get("logged_in"):
        return redirect("/")
    balance = get_wallet()
    return render_template("wallet.html", balance=balance)

@app.route("/chat")
def chat():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("chat.html")

@app.route("/drop")
def drop():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("drop.html")

@app.route("/casino")
def casino():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("casino.html")
