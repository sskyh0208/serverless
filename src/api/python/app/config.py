import os

ENV_NAME = os.environ['ENV_NAME']
AWS_REGION = os.environ['AWS_REGION']

DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL', None)

ALLOW_ORIGINS = os.environ['ALLOW_ORIGINS'].split(',')
ALLOW_CREDENTIALS = os.environ['ALLOW_CREDENTIALS'].lower() == 'true'
ALLOW_METHODS = os.environ['ALLOW_METHODS'].split(',')
ALLOW_HEADERS = os.environ['ALLOW_HEADERS'].split(',')

COGNITO_USER_POOL_ID = os.environ['COGNITO_USER_POOL_ID']
COGNITO_USER_POOL_CLIENT_ID = os.environ['COGNITO_USER_POOL_CLIENT_ID']