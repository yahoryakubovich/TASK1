import json


class JsonDataReader:
    @staticmethod
    def read(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
