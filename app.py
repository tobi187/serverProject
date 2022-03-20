from services.upload_service import get_ran_hash, create_output
import os
import tempfile

from flask import Flask, redirect, url_for, render_template, request, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

from services.auth_service import do_auth

app = Flask(__name__)
auth = HTTPBasicAuth()
ALLOWED_EXTENSION = "xlsx"
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")


app_data = {
    "name":         "Peter's Starter Template for a Flask Web App",
    "description":  "A basic Flask app using bootstrap for layout",
    "author":       "Peter Simeth",
    "html_title":   "Peter's Starter Template for a Flask Web App",
    "project_name": "Starter Template",
    "keywords":     "flask, webapp, template, basic"
}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == ALLOWED_EXTENSION


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


@app.route("/up", methods=["POST"])
def upload():
    if request.method == "POST":
        files = [f for f in request.files.values() if f.filename != ""]
        if len(files) < 1:
            return redirect(url_for("index"))

        for file in files:
            if not file or not allowed_file(file.filename):
                return redirect(url_for("index"))

        create_output(files)

        return redirect(url_for("download_file"))


@app.route("/download_file")
def download_file():
    return "<h1>Success</h1>"


if __name__ == '__main__':
    app.run(debug=True)
