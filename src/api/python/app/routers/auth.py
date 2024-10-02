from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import boto3
from botocore.exceptions import ClientError

from ..config import COGNITO_USER_POOL_ID, COGNITO_USER_POOL_CLIENT_ID

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Cognitoで認証するための設定
client = boto3.client('cognito-idp')

@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    try:
        response = client.admin_initiate_auth(
            UserPoolId=COGNITO_USER_POOL_ID,
            ClientId=COGNITO_USER_POOL_CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        print('login success')
    except Exception as e:
        print(f'login failed: {e}')
        return {
            "status_code": 400,
            "message": "Incorrect email or password"
        }
    
    return response

@router.get("/check-auth")
async def check_auth(token: str = Depends(oauth2_scheme)):
    try:
        # Cognitoを使用してトークンを検証
        response = client.get_user(AccessToken=token)
        
        # トークンが有効な場合、ユーザー情報を返す
        return {
            "status": "authenticated",
            "user": response['Username'],
            "user_attributes": {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        else:
            raise HTTPException(status_code=500, detail=str(e))