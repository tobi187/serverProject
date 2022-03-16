from flask import Flask, redirect, url_for, render_template, request
from flask_httpauth import HTTPBasicAuth
from services.auth_service import do_auth

app = Flask(__name__)
auth = HTTPBasicAuth()

app_data = {
    "name":         "Peter's Starter Template for a Flask Web App",
    "description":  "A basic Flask app using bootstrap for layout",
    "author":       "Peter Simeth",
    "html_title":   "Peter's Starter Template for a Flask Web App",
    "project_name": "Starter Template",
    "keywords":     "flask, webapp, template, basic"
}


@app.route("/")
def start():
    return redirect(url_for("index"))


@auth.verify_password
def verify_password(username, password):
    return do_auth(username, password)


@app.route("/overview/combine")
@auth.login_required()
def index():
    return render_template("index.html", app_data=app_data)


@app.route("/nooNeed", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        d = request.files
        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)