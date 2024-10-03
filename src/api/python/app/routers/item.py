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
        item = Item.get('item', item_id)
        
        return item.to_dict() if item else None
    except Exception as e:
        return {"error": str(e)}

@router.get("")
def get_category_items(category: str = Query(..., description="Category")):
    try:
        if category == 'all':
            category = None
        
        items = Item.query(
            'item',
            Item.SK.startswith(f'category_{category}') if category else None 
        )
        
        return [item.to_dict() for item in items]
    except Exception as e:
        return {"error": str(e)}