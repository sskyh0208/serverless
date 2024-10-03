from fastapi import APIRouter, Query

from ..models import Log

router = APIRouter()

@router.get("")
def get_logs(
    type: str = Query(None, description="ログの種類"),
    start_at: int = Query(None, description="開始日時"),
    end_at: int = Query(None, description="終了日時")
):
    """
    ログを取得します。
    
    Args:
        start_at (int): 開始日時
        end_at (int): 終了日時
        
    Returns:
        list: ログ情報のリスト
    """
    print(f'type: {type}, start_at: {start_at}, end_at: {end_at}')
    condition = [
        Log.SK.startswith(f"type_{type}") if type else Log.SK.startswith("type")
    ]
    
    if start_at and end_at:
        condition.append(Log.created_at.between(start_at, end_at))
    elif start_at:
        condition.append(Log.created_at >= start_at)
    elif end_at:
        condition.append(Log.created_at <= end_at)
    
    logs = Log.query(
        'log',
        *condition
    )
    
    return [log.to_dict() for log in logs]