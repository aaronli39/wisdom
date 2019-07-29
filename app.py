from flask import Flask
from os import urandom

from flask import request, render_template, redirect

app = Flask(__name__)

app.config["SECRET_KEY"] = urandom(32)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

