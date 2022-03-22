from flask import redirect, url_for, render_template, request, send_file, jsonify
from flask_httpauth import HTTPBasicAuth
from flaskr import tasks
from flaskr.services.upload_service import create_output
from  flaskr.services.auth_service import do_auth
from flask import Blueprint
import os
import io


auth = HTTPBasicAuth()
ALLOWED_EXTENSION = "xlsx"

app_data = {
    "name":         "Peter's Starter Template for a Flask Web App",
    "description":  "A basic Flask app using bootstrap for layout",
    "author":       "Peter Simeth",
    "html_title":   "Peter's Starter Template for a Flask Web App",
    "project_name": "Starter Template",
    "keywords":     "flask, webapp, template, basic"
}

bp = Blueprint("routes", __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == ALLOWED_EXTENSION


@auth.verify_password
def verify_password(username, password):
    return do_auth(username, password)


@bp.route("/")
def start():
    return redirect(url_for("routes.index"))


@bp.route("/overview/combine")
@auth.login_required()
def index():
    return render_template("index.html", app_data=app_data)


@bp.route("/up", methods=["POST"])
def upload():
    if request.method == "POST":
        files = [f for f in request.files.values() if f.filename != ""]
        if len(files) < 1:
            return redirect(url_for("routes.index"))

        for file in files:
            if not file or not allowed_file(file.filename):
                return redirect(url_for("routes.index"))

        # file_name = create_output(files, os.getcwd())
        #
        # return redirect(url_for("routes.download_file", name=file_name))

        tasks.create_task.delay(files)

        return "<h1>Loading</h1>"


@bp.route("/download_file/<name>")
def download_file(name: str):
    exel_data = io.BytesIO()
    file_path = os.path.join(os.getcwd(), "uploads", name)

    with open(file_path, "rb") as data:
        exel_data.write(data.read())
        exel_data.seek(0)

    os.remove(file_path)

    return send_file(exel_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     download_name='combined_reports.xlsx')
