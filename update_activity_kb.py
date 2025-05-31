import requests
import json
import os

headers = {"Authorization": f"Bearer {os.environ['KB_API_KEY'].strip()}"}
file_path = "crawler/output/activity/activity_result.txt"
url = f"{os.environ['DIFY_BASE_URL']}/datasets/{os.environ['DATASET_ID']}/documents/{os.environ['DOCUMENT_ID']}/update-by-file"

with open(file_path, "rb") as f:
    files = {"file": f}
    data = {
        "name": "activity_result.txt",
        "indexing_technique": "high_quality",
        "process_rule": {
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": False},
                ],
                "segmentation": {
                    "separator": "=END=",
                    "max_tokens": 4000,
                },
            },
            "mode": "custom",
        },
    }
    # Dify API 要求 data 必須是 JSON 字串
    response = requests.post(
        url, headers=headers, files=files, data={"data": json.dumps(data)}
    )
    print(response.status_code, response.text)
