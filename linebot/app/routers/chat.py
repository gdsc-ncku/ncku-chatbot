from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.get("/")
async def chat():
    return {"message": "Hello World, this is chat router"}