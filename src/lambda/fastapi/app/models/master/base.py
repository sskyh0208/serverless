from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from datetime import datetime
from ...config import ENV_NAME, AWS_DYNAMODB_ENDPOINT_URL, AWS_REGION, DYNAMODB_MASTER_TABLE_NAME

class MasterTableModel(Model):
    class Meta:
        table_name = DYNAMODB_MASTER_TABLE_NAME
        region = AWS_REGION
        host = AWS_DYNAMODB_ENDPOINT_URL

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute(default=datetime.now())
    updated_at = UTCDateTimeAttribute(default=datetime.now())
    
    def to_dict(self):
        return self.attribute_values