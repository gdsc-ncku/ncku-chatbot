# use app routers
from fastapi import FastAPI
from app.routers import chat, linebot

app = FastAPI()

@app.get("/")   
def read_root():
    return {"message": "Hello World"}

app.include_router(chat.router)
app.include_router(linebot.router)