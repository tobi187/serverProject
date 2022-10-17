import dataclasses
import json


@dataclasses.dataclass
class FileData:
    name: str
    author: str
    ending: str  # DateiEndung: txt, pptx usw.
    date: str

    def create_json(self):
        return {
            "name": self.name,
            "author": self.author,
            "ending": self.ending,
            "date": self.date
        }


def read_file_data(file_data):
    return FileData(
        name=file_data["name"],
        author=file_data["author"],
        ending=file_data["ending"],
        date=file_data["data"]
    )
