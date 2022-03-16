import pandas as pd
from ex_worker import ExcelWorker


def workflow(paths):
    excel_worker = ExcelWorker()
    excel_worker.setup()
    for file in paths:
        wb = pd.ExcelFile(file)
        for sheet in wb.sheet_names:
            sheet_df = pd.read_excel(file, engine="openpyxl", sheet_name=sheet)
            excel_worker.write_data(sheet_df)



