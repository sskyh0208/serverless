from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def health_check():
    print('health check')
    return {"status": "ok"}