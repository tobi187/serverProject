import os
import tempfile
import pandas as pd
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logic_combine_reports.ex_worker as excel_logic
import string
import random


def get_ran_hash(length) -> str:
    phrase = [random.choice(string.ascii_letters) for i in range(length)]
    return "".join(phrase)


def create_output(data_list: list[FileStorage], base_path: str) -> str:

    file_name = get_ran_hash(10) + ".xlsx"

    with tempfile.TemporaryDirectory() as folder:

        paths = []

        for data in data_list:
            path = os.path.join(folder, secure_filename(data.filename))
            data.save(path)
            paths.append(path)
        # excel_logic.workflow(paths)

        excel_worker = excel_logic.ExcelWorker(file_name, base_path)

        for file in paths:
            wb = pd.ExcelFile(file, engine="openpyxl")
            for sheet in wb.sheet_names:
                sheet_df = pd.read_excel(file, engine="openpyxl", sheet_name=sheet)
                excel_worker.write_data(sheet_df)
            wb.close()

    return file_name
