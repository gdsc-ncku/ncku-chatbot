import os
import json
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
URL = "https://dify-ncku-chatbot.yenslife.top/v1"  # 一定要用 https
headers = {
    "Authorization": f"Bearer {DIFY_API_KEY}",
}


def create_document_from_file(
    dataset_id: str,
    file_path: str,
    name: Optional[str] = None,
    indexing_technique: str = "high_quality",
    doc_form: str = "economy",
    process_rule: Optional[dict] = None,
):
    if process_rule is None:
        process_rule = {
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": True},
                ],
                "segmentation": {
                    "separator": "\n\n",
                    "max_tokens": 500,
                    "mode": "custom",
                },
            },
            "mode": "custom",
        }

    api_data = {
        "indexing_technique": indexing_technique,
        "doc_form": doc_form,
        "process_rule": process_rule,
    }
    form_data = {
        "data": json.dumps(api_data),
    }
    if name:
        form_data["name"] = name

    files = {"file": (os.path.basename(file_path), open(file_path, "rb"))}

    api_url = f"{URL}/datasets/{dataset_id}/document/create-by-file"
    try:
        response = requests.post(
            api_url,
            headers=headers,
            data=form_data,
            files=files,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating document: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response body: {e.response.text}")
        return None
    finally:
        if "file" in files:
            files["file"][1].close()


def get_knowledge_base_list():
    response = requests.get(
        f"{URL}/datasets",
        headers={
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with open("knowledge_base_list.json", "w") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error writing knowledge_base_list.json: {e}")
    except requests.exceptions.JSONDecodeError:
        print(f"Error decoding JSON from knowledge base list response: {response.text}")

    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting knowledge base list: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response body: {e.response.text}")
        return None
    except requests.exceptions.JSONDecodeError:
        print(f"Invalid JSON received for knowledge base list: {response.text}")
        return None


def get_knowledge_base_detail_by_id(dataset_id: str):
    api_url = f"{URL}/datasets/{dataset_id}"
    try:
        response = requests.get(
            api_url,
            headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting knowledge base detail for ID {dataset_id}: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response body: {e.response.text}")
        return None
    except requests.exceptions.JSONDecodeError:
        print(
            f"Invalid JSON received for knowledge base detail {dataset_id}: {response.text}"
        )
        return None


def delete_document(dataset_id: str, document_id: str):
    api_url = f"{URL}/datasets/{dataset_id}/documents/{document_id}"
    try:
        response = requests.delete(
            api_url,
            headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        print(f"Successfully deleted document {document_id} from dataset {dataset_id}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error deleting document {document_id} from dataset {dataset_id}: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response body: {e.response.text}")
        return None


def get_document_list_from_knowledge_base(
    dataset_id: str, page: int = 1, limit: int = 100
):
    api_url = f"{URL}/datasets/{dataset_id}/documents"
    try:
        response = requests.get(
            api_url,
            headers={
                "Authorization": f"Bearer {DIFY_API_KEY}",
                "Content-Type": "application/json",
            },
            params={
                "page": page,
                "limit": limit,
            },
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting document list for dataset {dataset_id}: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response body: {e.response.text}")
        return None
    except requests.exceptions.JSONDecodeError:
        print(f"Invalid JSON received for document list {dataset_id}: {response.text}")
        return None


def get_all_document_id_from_knowledge_base(dataset_id: str):
    all_documents = []
    page = 1
    limit = 100
    has_more = True
    while has_more:
        document_list = get_document_list_from_knowledge_base(dataset_id, page, limit)
        all_documents.extend(document_list["data"])
        has_more = document_list["has_more"]
        page += 1
    return [document["id"] for document in all_documents]
