from fastapi import APIRouter, Request, HTTPException
from linebot.exceptions import InvalidSignatureError
from ..config.line_config import handler

router = APIRouter(
    prefix="/linebot",
    tags=["linebot"]
)

@router.post("/webhook")
async def line_webhook(request: Request):
    # 獲取 X-Line-Signature header 值
    signature = request.headers['X-Line-Signature']
    
    # 獲取請求體內容
    body = await request.body()
    
    try:
        # 驗證簽名並處理請求
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    return 'OK'