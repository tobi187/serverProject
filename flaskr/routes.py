import tempfile
from flask import redirect, url_for, render_template, request, send_file, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from flaskr import tasks
from flaskr.services.upload_service import create_output
from flaskr.services.auth_service import do_auth
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


@bp.route("/overview/combine", methods=["GET", "POST"])
@auth.login_required()
def index():

    if request.method == "POST":
        files = [f for f in request.files.values() if f.filename != ""]
        if len(files) < 1:
            return redirect(url_for("routes.index"))

        for file in files:
            if not file or not allowed_file(file.filename):
                return redirect(url_for("routes.index"))

        paths = []
        tempdir = tempfile.mkdtemp(dir=os.path.join(os.getcwd(), "temp"))
        for file in files:
            path = os.path.join(tempdir, secure_filename(file.filename))
            file.save(path)
            paths.append(path)

        task = tasks.create_task.delay(paths, tempdir)

        return render_template("index.html", app_data=app_data, dl=url_for("routes.get_status", task_id=task.id))

    return render_template("index.html", app_data=app_data, dl="")


# @bp.route("/up", methods=["POST"])
# def upload():
#     if request.method == "POST":
#         files = [f for f in request.files.values() if f.filename != ""]
#         if len(files) < 1:
#             return redirect(url_for("routes.index"))
#
#         for file in files:
#             if not file or not allowed_file(file.filename):
#                 return redirect(url_for("routes.index"))
#
#         # file_name = create_output(files, os.getcwd())
#         #
#         # return redirect(url_for("routes.download_file", name=file_name))
#
#         paths = []
#         tempdir = tempfile.mkdtemp(dir=os.path.join(os.getcwd(), "temp"))
#         for file in files:
#             path = os.path.join(tempdir, secure_filename(file.filename))
#             file.save(path)
#             paths.append(path)
#
#         task = tasks.create_task.delay(paths, tempdir)
#
#         return redirect(url_for("routes.index"), download_link=url_for("routes.get_status", task_id=task.id)))


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

# b


@bp.route("/dl_test/<name>")
def dl_test(name: str):
    # name = request.form["file_name"]
    exel_data = io.BytesIO()
    file_path = os.path.join(os.getcwd(), "uploads", name)

    with open(file_path, "rb") as data:
        exel_data.write(data.read())
        exel_data.seek(0)

    os.remove(file_path)

    return send_file(exel_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     download_name='combined_reports.xlsx')


@bp.route("/status/<task_id>")
def get_status(task_id):
    task = tasks.create_task.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"state": task.state, "current": 0,
                    "total": 0, "status": "Waiting"}
    elif task.state != "FAILURE":
        response = {"state": task.state, "current": task.info.get("current", 0),
                    "total": task.info.get("total", 0), "status": task.info.get("status", "?")}
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }

    return jsonify(response)
