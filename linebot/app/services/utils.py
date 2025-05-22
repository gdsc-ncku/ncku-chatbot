import json


def flex_message_convert_to_json(file_path):
    with open(file_path, "r") as f:
        flex_message = json.load(f)
    return flex_message
