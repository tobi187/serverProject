import os

from flask import Flask, redirect, url_for, render_template, request, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

from services.auth_service import do_auth

app = Flask(__name__)
auth = HTTPBasicAuth()
UPLOAD_FOLDER = r'/uploads'
ALLOWED_EXTENSIONS = ["xlsx"]
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@app.route("/up/", methods=["POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))


if __name__ == '__main__':
    app.run(debug=True)