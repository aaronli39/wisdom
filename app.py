from flask import Flask
from os import urandom

from flask import request, render_template, redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = urandom(32)

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/admin")
def admin():
    return render_template("admin_home.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

