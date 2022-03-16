import pandas as pd
from ex_worker import ExcelWorker
from time import time


def workflow(save_file, paths):
    excel_worker = ExcelWorker(save_file)
    excel_worker.setup()
    for file in paths:
        wb = pd.ExcelFile(file)
        for sheet in wb.sheet_names:
            sheet_df = pd.read_excel(file, engine="openpyxl", sheet_name=sheet)
            excel_worker.write_data(sheet_df)


def start():
    files = sg.popup_get_file("Wähle die Excel Dateien aus denen der Report erstellt werden soll\n(Namen dürfen keine Strickpunkte enthalten)", title="ReportAutomation", multiple_files=True, file_types=(("Excel", "*.xlsx"),))
    save_file_path = sg.popup_get_file("Wähle die Datei zum Speichern aus\nBitte schliesse alle Excel Files die du jetzt und vorher ausgewählt hast\nWenn du auf OK drückst startet das Programm", title="ReportAutomation")
    if files != "" and files is not None and save_file_path != "" and save_file_path is not None:
        files = files.split(";")
        start = time()
        workflow(save_file_path, files)
        sg.PopupOK(f"Fertig\nDauer: {time() - start}")
