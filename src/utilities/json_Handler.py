# WIP
import json

class JsonHandler:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Arquivo {self.file_path} não encontrado.")
            return None
        except json.JSONDecodeError:
            print("Erro ao decodificar o JSON.")
            return None