from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute

from . import MasterTableModel

class Item(MasterTableModel):

    id = UnicodeAttribute()
    category_id = UnicodeAttribute()
    name = UnicodeAttribute()
    description = UnicodeAttribute()
    price = NumberAttribute()
    deleted_at = UTCDateTimeAttribute()