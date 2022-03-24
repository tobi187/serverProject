import os
import shutil
import tempfile
import pandas as pd
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flaskr.logic.combine_reports import ex_worker as excel_logic
import string
import random
import warnings


def get_ran_hash(length) -> str:
    phrase = [random.choice(string.ascii_letters) for _ in range(length)]
    return "".join(phrase)


def create_output(paths: list[str], tp) -> str:

    file_name = get_ran_hash(10) + ".xlsx"

    # TODO: probably should change that some time
    warnings.simplefilter("ignore")

    # with tempfile.TemporaryDirectory() as folder:

        # paths = []
        #
        # for data in data_list:
        #     path = os.path.join(folder, secure_filename(data.filename))
        #     data.save(path)
        #     paths.append(path)
        # # excel_logic.workflow(paths)

    excel_worker = excel_logic.ExcelWorker(file_name, os.getcwd())

    for file in paths:
        wb = pd.ExcelFile(file, engine="openpyxl")
        for sheet in wb.sheet_names:
            sheet_df = pd.read_excel(file, engine="openpyxl", sheet_name=sheet)
            excel_worker.write_data(sheet_df)
        wb.close()

    shutil.rmtree(tp)

    return file_name
