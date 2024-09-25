import os
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
            return
        except json.JSONDecodeError:
            print("Erro ao decodificar o JSON.")

    def write(self, data, indent: int = 2):
        if not self.file_path.endswith(".json"):
            self.file_path = self.file_path+".json"

        try:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=indent)
        except Exception as e:
            print(f"Erro ao escrever no arquivo: {e}")

    def update(self, key, value):
        data = self.read()
        if data:
            data[key] = value
            self.write(data)

    def delete_key(self, key):
        data = self.read()
        if data and key in data:
            del data[key]
            self.write(data)

    def delete_file(self):
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            print(f"Arquivo {self.file_path} não encontrado.")
            return
        except Exception as e:
            print(f"Erro ao apagar o arquivo: {e}")