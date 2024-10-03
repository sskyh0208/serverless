from pynamodb.attributes import UnicodeAttribute

from . import TransactionTableModel

class Log(TransactionTableModel):
    
    id = UnicodeAttribute()
    type = UnicodeAttribute()
    user_id = UnicodeAttribute()
    item_id = UnicodeAttribute()
    