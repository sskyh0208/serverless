from aws_cdk import (
    Stack,
    RemovalPolicy,
    Tags,
    BundlingFileAccess,
    CfnOutput,
    aws_s3 as s3,
    aws_lambda_python_alpha as lambda_python,
    aws_apigateway as apigateway,
    aws_ecr as ecr,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_cognito as cognito,
)
from aws_cdk.aws_lambda import Runtime, DockerImageCode, DockerImageFunction
from aws_cdk.aws_ecr_assets import DockerImageAsset, Platform
from constructs import Construct
import os

class MainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        params = kwargs.pop('params', None)
        
        super().__init__(scope, construct_id, **kwargs)
        ######################################################################
        # 共通の環境変数
        ######################################################################
        
        product_name = params.get('product_name')
        env_name = params.get('env_name')
        account_id = self.account
        region = self.region
        
        prefix_name = f'{product_name}-{env_name}'
        
        lambda_base_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'lambda'))
        
        # ######################################################################
        # # S3
        # ######################################################################
        # s3_common = s3.Bucket(self,
        #     id='S3CommonBucket',
        #     bucket_name=f'{prefix_name}-s3-common-{account_id}',
        #     versioned=False,
        #     removal_policy=RemovalPolicy.DESTROY,
        # )
        
        # Tags.of(s3_common).add('Name', f'{prefix_name}-s3-common-{account_id}')
        # Tags.of(s3_common).add('Product', product_name)
        # Tags.of(s3_common).add('Env', env_name)
        
        # CfnOutput(
        #     self, 'S3CommonBucketName',
        #     value=s3_common.bucket_name
        # )
        
        # CfnOutput(
        #     self, 'S3CommonBucketArn',
        #     value=s3_common.bucket_arn
        # )
        
        ######################################################################
        # DynamoDB
        ######################################################################
        master_table = dynamodb.TableV2(self,
            id='MasterTable',
            table_name=f'{prefix_name}-dynamodb-master',
            partition_key=dynamodb.Attribute(
                name='PK',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='SK',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing=dynamodb.Billing.on_demand(),
        )
        
        transaction_table = dynamodb.TableV2(self,
            id='TransactionTable',
            table_name=f'{prefix_name}-dynamodb-transaction',
            partition_key=dynamodb.Attribute(
                name='PK',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='SK',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing=dynamodb.Billing.on_demand(),
        )
        
        ######################################################################
        # IAM
        ######################################################################
        iam_lambda_fastapi = iam.Role(self,
            id='IamLambdaFastApi',
            role_name=f'{prefix_name}-role-lambda-fastapi',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            ]
        )
        
        iam_lambda_fastapi.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    'dynamodb:Query',
                    'dynamodb:Scan',
                    'dynamodb:GetItem',
                    'dynamodb:PutItem',
                    'dynamodb:UpdateItem',
                    'dynamodb:DeleteItem',
                ],
                resources=[
                    master_table.table_arn,
                    transaction_table.table_arn,
                ]
            )
        )
        
        ######################################################################
        # Lambda (Image)
        ######################################################################
        ecr_fastapi = ecr.Repository(self,
            id='EcrFastApi',
            repository_name=f'{prefix_name}-ecr-fastapi',
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            removal_policy=RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )
        
        ecr_fastapi.add_lifecycle_rule(
            max_image_count=5,
            rule_priority=1,
            description='keep 5 images',
        )
        
        lambda_fastapi = DockerImageFunction(self,
            id='LambdaFastApi',
            function_name=f'{prefix_name}-function-fastapi',
            description='fastapi lambda function',
            memory_size=256,
            role=iam_lambda_fastapi,
            environment={
                'ENV_NAME': env_name,
                'ALLOW_ORIGINS': '*',
                'ALLOW_CREDENTIALS': 'True',
                'ALLOW_METHODS': '*',
                'ALLOW_HEADERS': '*',
                'COGNITO_USER_POOL_ID': 'dummy',
                'COGNITO_USER_POOL_CLIENT_ID': 'dummy',
                'DYNAMODB_MASTER_TABLE_NAME': master_table.table_name,
                'DYNAMODB_TRANSACTION_TABLE_NAME': transaction_table.table_name,
            },
            code=DockerImageCode.from_image_asset(
                directory=os.path.join(lambda_base_dir_path, 'fastapi'),
                file='Dockerfile',
                target=env_name,
                platform=Platform.LINUX_AMD64,
                exclude=['*', '!app', '!poetry.lock', '!pyproject.toml']
            )
        )
        
        
        CfnOutput(
            self, 'LambdaFunctionImageArn',
            value=lambda_fastapi.function_arn
        )
        
        CfnOutput(
            self, 'LambdaFunctionImageName',
            value=lambda_fastapi.function_name
        )
        
        ######################################################################
        # API Gateway
        ######################################################################
        api_backend = apigateway.RestApi(self,
            id='ApiGateway',
            rest_api_name=f'{prefix_name}-api-backend',
            description='backend api',
            deploy_options={
                'stage_name': 'v1'
            }
        )
        
        # /{proxy+}で全てのリクエストをLambdaに流す
        api_backend.root.add_resource('{proxy+}').add_method('ANY', apigateway.LambdaIntegration(lambda_fastapi))
        
        Tags.of(api_backend).add('Name', f'{prefix_name}-api-backend')
        Tags.of(api_backend).add('Product', product_name)
        Tags.of(api_backend).add('Env', env_name)
        
        CfnOutput(
            self, 'ApiGatewayId',
            value=api_backend.rest_api_id
        )
        
        CfnOutput(
            self, 'ApiGatewayHealthCheckUrl',
            value=f'{api_backend.url}/health_check'
        )
            
        ######################################################################
        # Cognito
        ######################################################################
        cognito_user_pool = cognito.UserPool(self,
            id='CognitoUserPool',
            user_pool_name=f'{prefix_name}-cognito-user-pool',
            removal_policy=RemovalPolicy.DESTROY,
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                email=True
            ),
            auto_verify=cognito.AutoVerifiedAttrs(
                email=True
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                )
            )
        )
        
        cognito_user_pool_client = cognito.UserPoolClient(self,
            id='CognitoUserPoolClient',
            user_pool_client_name=f'{prefix_name}-cognito-user-pool-client',
            user_pool=cognito_user_pool,
            auth_flows=cognito.AuthFlow(
                admin_user_password=True,
                custom=False,
                user_password=True,
                user_srp=True
            ),
            generate_secret=False
        )