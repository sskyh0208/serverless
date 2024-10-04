from fastapi import APIRouter, Query

from ..models import Item

router = APIRouter()

@router.get("")
async def get_items(
    category_id: str = Query(None, description="カテゴリー ID"),
):
    conditions = [
        'item',
        Item.SK.startswith(f'item_')
    ]
    
    if category_id:
        conditions.append(Item.category_id == category_id)
        
    try:
        items = Item.query(
            *conditions
        )
        
        return [item.to_dict() for item in items]
    except Exception as e:
        return {"error": str(e)}

@router.get("/{item_id}")
async def get_item(item_id: str):
    try:
        item = Item.query(
            'item',
            Item.SK.startswith(f'item_{item_id}_')
        )
        
        return [item.to_dict() for item in item][0] if item else {}
    except Exception as e:
        return {"error": str(e)}