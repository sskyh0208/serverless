from fastapi import APIRouter, Query

from ..models import Item

router = APIRouter()

@router.get("")
def get_items():
    try:
        items = Item.query(
            'item'
        )
        
        return [item.to_dict() for item in items]
    except Exception as e:
        return {"error": str(e)}

@router.get("/{item_id}")
def get_item(item_id: str):
    try:
        item = Item.query(
            'item',
            Item.SK.startswith(f'item_{item_id}_')
        )
        
        return [item.to_dict() for item in item][0]
    except Exception as e:
        return {"error": str(e)}

@router.get("/category/{category_id}")
def get_category_items(category_id: str):
    try:
        
        items = Item.query(
            'item',
            Item.SK.startswith(f'item_'),
            Item.category_id == category_id
        )
        
        return [item.to_dict() for item in items]
    except Exception as e:
        return {"error": str(e)}