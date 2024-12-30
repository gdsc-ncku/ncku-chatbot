# use app routers
from fastapi import FastAPI
from app.routers import linebot
from app import webhooks  # 導入 handlers
from app.db.database import engine
from app.models import user

# 創建數據庫表
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")   
def read_root():
    return {"message": "Hello World"}

app.include_router(linebot.router)