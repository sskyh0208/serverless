from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from datetime import datetime
from ...config import ENV_NAME, DYNAMODB_ENDPOINT_URL, AWS_REGION

class TransactionTableModel(Model):
    class Meta:
        table_name = f'{ENV_NAME}_transaction'
        region = AWS_REGION
        host = DYNAMODB_ENDPOINT_URL

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute(default=datetime.now())
    
    def to_dict(self):
        return self.attribute_values