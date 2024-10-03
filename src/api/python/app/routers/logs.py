from fastapi import APIRouter, Query, HTTPException

from ..models import Log

router = APIRouter()

@router.get("")
async def get_logs(
    type_id: str = Query(None, description="ログの種類"),
    start_at: int = Query(None, description="開始日時"),
    end_at: int = Query(None, description="終了日時"),
    user_id: str = Query(None, description="ユーザー ID"),
    item_id: str = Query(None, description="アイテム ID"),
):  
    try:
        condition = [
            'log',
            Log.SK.startswith('type_')
        ]
        
        if type_id:
            condition.append(Log.type_id == type_id)
        
        if start_at and end_at:
            condition.append(Log.created_at.between(start_at, end_at))
        elif start_at:
            condition.append(Log.created_at >= start_at)
        elif end_at:
            condition.append(Log.created_at <= end_at)
        
        if user_id:
            condition.append(Log.user_id == user_id)
        if item_id:
            condition.append(Log.item_id == item_id)
        
        logs = Log.query(
            *condition
        )
        
        return [log.to_dict() for log in logs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))