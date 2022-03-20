import os.path
import tempfile
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logic_combine_reports.ex_worker as excel_logic
import string
import random


def get_ran_hash(length) -> str:
    phrase = [random.choice(string.ascii_letters) for i in range(length)]
    return "".join(phrase)


def create_output(data_list: list[FileStorage]):

    with tempfile.TemporaryDirectory() as folder:
        paths = []
        for data in data_list:
            path = os.path.join(folder, secure_filename(data.filename))
            data.save(path)
            paths.append(path)
        excel_logic.workflow(paths)
