from aws_cdk import App, Environment
from aws_cdk.assertions import Template
from src.main import MainStack
import os
import sys

def test_main_stack():
    app = cdk.App()

    main_stack = MainStack(
        scope=app,
        construct_id='test-main',
        params={
            'product_name': 'test-product',
            'env_name': 'test-env',
            'account_id': 'test-account-id'
        }
    )
    
    template = Template.from_stack(main_stack)
    
    # テスト: S3 バケットが正しく作成されているか
    template.has_resource_properties('AWS::S3::Bucket', {
        "BucketName": "test-product-test-env-s3-common-test-account-id"
    })

    # テスト: Lambda 関数が正しく作成されているか
    template.has_resource_properties('AWS::Lambda::Function', {
        "Handler": "main.lambda_handler",
        "Runtime": "python3.12"
    })