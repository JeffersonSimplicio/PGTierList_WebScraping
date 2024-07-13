# WIP
import json

def write_to_json_file (
    file_name: str,
    data
) -> None:
    if not file_name.endswith(".json"):
        file_name = file_name+".json"
    with open(file_name, 'w') as file:
        json.dump(data, file)