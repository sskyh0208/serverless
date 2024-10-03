#!/bin/sh

# テーブル作成
aws dynamodb create-table --table-name local_master \
  --region ap-northeast-1 \
  --endpoint-url http://dynamodb-local:8000 \
  --attribute-definitions \
    AttributeName=PK,AttributeType=S \
    AttributeName=SK,AttributeType=S \
  --key-schema \
    AttributeName=PK,KeyType=HASH \
    AttributeName=SK,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --no-cli-pager;

aws dynamodb create-table --table-name local_transaction \
  --region ap-northeast-1 \
  --endpoint-url http://dynamodb-local:8000 \
  --attribute-definitions \
    AttributeName=PK,AttributeType=S \
    AttributeName=SK,AttributeType=S \
  --key-schema \
    AttributeName=PK,KeyType=HASH \
    AttributeName=SK,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --no-cli-pager;

# データ追加
aws dynamodb put-item --table-name local_master \
  --region ap-northeast-1 \
  --endpoint-url http://dynamodb-local:8000 \
  --no-cli-pager \
  --item '
  {
    "PK": {"S": "item"},
    "SK": {"S": "item_1_category_食料品"},
    "id": {"S": "1"},
    "name": {"S": "お米"},
    "category": {"S": "食料品"},
    "description": {"S": "お米です"},
    "price": {"N": "1000"}
  }';

aws dynamodb put-item --table-name local_transaction \
  --region ap-northeast-1 \
  --endpoint-url http://dynamodb-local:8000 \
  --no-cli-pager \
  --item '
  {
    "PK": {"S": "log"},
    "SK": {"S": "type_1"},
    "id": {"S": "1"},
    "type": {"S": "1"},
    "user_id": {"S": "1"},
    "item_id": {"S": "1"}
  }';