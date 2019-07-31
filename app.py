import json
from os import urandom

from flask import Flask, request, render_template, redirect
from util import Database

config = json.load(open("config/mongo.json"))

app = Flask(__name__)

app.config["MONGO_DBNAME"] = config['databaseName']
app.config["MONGO_URI"] = config['mongoURI']
app.config["SECRET_KEY"] = urandom(32)

dbtools = Database.DBTools(app)

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login")
def log():
    return render_template("login.html")

@app.route("/register")
def reg():
    return render_template("register.html")

@app.route("/admin")
def admin():
    return render_template("admin_home.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

