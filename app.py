from flask import Flask, redirect, url_for, render_template, request, send_file, flash, send_from_directory
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from services.auth_service import do_auth
import os


app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")


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


@app.route("/up", methods=["POST"])
def upload():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("index"))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("index"))
        if file:
            name = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], name))

            return redirect(url_for("download_file", name=name))


@app.route("/download_file/<name>")
def download_file(name: str):

    return send_from_directory()


if __name__ == '__main__':
    app.run()
