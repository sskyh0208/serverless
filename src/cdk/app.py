from aws_cdk import App, Environment
from src.main import MainStack
import os
import sys

app = App()

environment = app.node.try_get_context('environment')
if environment is None:
    raise ValueError('環境変数が設定されていません。例) cdk deploy -c environment=dev')

env_values = app.node.try_get_context(environment)

# 共通の環境変数
ENV = Environment(**env_values.get('env'))
PRODUCT_NAME = app.node.try_get_context('product_name')
ENV_NAME = env_values.get('env_name')
ACCOUNT_ID = env_values.get('env').get('account')
BASE_PARAMS = {
    'product_name': PRODUCT_NAME,
    'env_name': ENV_NAME,
    'account_id': ACCOUNT_ID
}

################################################################################
# MainStack
################################################################################
params = {}
params.update(BASE_PARAMS)
MainStack(
    scope=app,
    construct_id=f'{PRODUCT_NAME}-{ENV_NAME}-main',
    env=ENV,
    description=f'{PRODUCT_NAME} {ENV_NAME} main stack',
    params=params
)

app.synth()