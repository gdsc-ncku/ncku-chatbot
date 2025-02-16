from __future__ import print_function
import os.path
from fastapi import FastAPI, HTTPException, Query
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any
from rich import print

app = FastAPI()

# 如果修改了 SCOPES，請刪除 token.json 檔案。
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly']

def get_spreadsheet_data_from_drive(folder_id: str) -> List[Dict[str, Any]]:
    """
    從指定 Google Drive 資料夾中的所有試算表取得資料。
    Returns:
        List[Dict[str, Any]]: 包含每個試算表資料的列表。
        每個字典包含 'name', 'id', 和 'data' 鍵。
        'data' 是一個列表，其中每個元素代表試算表的一列。
    Raises:
        HTTPException: 如果發生任何錯誤，會拋出 HTTPException。
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)

        query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            raise HTTPException(status_code=404, detail=f"在資料夾 ID '{folder_id}' 中找不到試算表檔案。")

        spreadsheet_data_list = []
        for file in files:
            spreadsheet_id = file['id']
            spreadsheet_name = file['name']

            range_name = 'A1:ZZZ'
            sheet = sheets_service.spreadsheets()
            values_result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = values_result.get('values', [])

            spreadsheet_data_list.append({
                "name": spreadsheet_name,
                "id": spreadsheet_id,
                "data": values if values else [] # 如果沒有資料，則返回空列表
            })

        return spreadsheet_data_list

    except HttpError as error:
        raise HTTPException(status_code=500, detail=f"發生 Google API 錯誤: {error}")

@app.get("/get_sheets")
async def get_sheets_api(folder_id: str = Query(..., title="Folder ID", description="您的 Google Drive 資料夾 ID")):
    """
    API 端點，用於取得指定 Google Drive 資料夾中所有試算表的資料。
    - **folder_id**:  您的 Google Drive 資料夾 ID (字串)。
    """
    try:
        spreadsheet_data = get_spreadsheet_data_from_drive(folder_id)
        return {"message": "成功取得試算表資料", "data": spreadsheet_data}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"伺服器內部錯誤: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)