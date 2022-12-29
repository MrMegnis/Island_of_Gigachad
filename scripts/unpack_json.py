import json

def unpack_json(path:str)->dict:

    with open(path, encoding="utf-8") as file:
        return json.load(file)