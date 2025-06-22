from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os, importlib
from wallet import get_wallet, update_balance

app = Flask(__name__)
app.secret_key = "dah_secret_key"

PLUGINS_FOLDER = "plugins"
PLUGINS = {}

for file in os.listdir(PLUGINS_FOLDER):
    if file.endswith(".py"):
        module_name = file[:-3]
        module = importlib.import_module(f"{PLUGINS_FOLDER}.{module_name}")
        PLUGINS[module_name.lower()] = module

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST" and request.form.get("password") == "dahonly":
        session["logged_in"] = True
        return redirect("/home")
    return render_template("login.html")

@app.route("/home")
def home():
    if not session.get("logged_in"): return redirect("/")
    return render_template("home.html")

@app.route("/bots")
def bots():
    if not session.get("logged_in"): return redirect("/")
    return render_template("bots.html", tools=PLUGINS.keys())

@app.route("/chat")
def chat():
    if not session.get("logged_in"): return redirect("/")
    return render_template("chat.html")

@app.route("/wallet")
def wallet():
    if not session.get("logged_in"): return redirect("/")
    return render_template("wallet.html", data=get_wallet())

@app.route("/casino")
def casino():
    if not session.get("logged_in"): return redirect("/")
    return render_template("casino.html")

@app.route("/drop")
def drop():
    if not session.get("logged_in"): return redirect("/")
    return render_template("drop.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    tool = data.get("tool", "").lower()
    if tool in PLUGINS:
        try:
            output = PLUGINS[tool].run()
            return jsonify({"output": output})
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify({"error": "Tool not found"})

if __name__ == "__main__":
    app.run(debug=True)
