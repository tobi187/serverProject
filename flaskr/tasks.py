import os
import random
# import secrets
import string
import tempfile
import pandas as pd
from celery import Celery
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, redirect
# from logic.combine_reports import ex_worker
from flask import url_for
from flaskr.services.upload_service import create_output

celery = Celery(__name__)

celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


@celery.task()
def create_task(data_list: list[FileStorage]):
    # # file_name = secrets.token_hex(8)
    # file_name = "".join([random.choice(string.ascii_letters) for _ in range(10)])
    #
    # with tempfile.TemporaryDirectory() as folder:
    #     paths = []
    #
    #     # self.update_state(state='WORKING',
    #     #                   meta={'current': 0, 'total': len(data_list),
    #     #                         'status': "Daten einlesen"})
    #
    #     for data in data_list:
    #         path = os.path.join(folder, secure_filename(data.filename))
    #         data.save(path)
    #         paths.append(path)
    #     # excel_logic.workflow(paths)
    #
    #     excel_worker = ex_worker.ExcelWorker(file_name, os.getcwd())
    #
    #     counter = 1
    #
    #     for file in paths:
    #         # self.update_state(state='WORKING',
    #         #                   meta={'current': counter, 'total': len(data_list),
    #         #                         'status': "Daten zusammenfügen"})
    #         counter += 1
    #         wb = pd.ExcelFile(file, engine="openpyxl")
    #         for sheet in wb.sheet_names:
    #             sheet_df = pd.read_excel(file, engine="openpyxl", sheet_name=sheet)
    #             excel_worker.write_data(sheet_df)
    #         wb.close()

    file_name = create_output(data_list, os.getcwd())

    return redirect(url_for("routes.download_file", name=file_name))
    # return {"current": len(data_list), "total": len(data_list),
    #         "status": "Completed", "result": url_for("routes.download_file", name=file_name)}
