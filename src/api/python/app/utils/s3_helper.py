# app/utils/s3_helper.py
import os
import boto3
from botocore.client import Config

def get_s3_client():
    # クライアント設定用の辞書を初期化
    s3_params = {
        'service_name': 's3',
        'region_name': os.getenv('AWS_REGION')
    }
    
    # ローカル MinIO を使用する場合のみ追加の設定をする
    if os.getenv('USE_LOCAL_MINIO', 'false').lower() == 'true':
        s3_params.update({
            'endpoint_url': os.getenv('MINIO_ENDPOINT'),
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'config': Config(signature_version='s3v4')
        })
    
    # クライアントを作成して返す
    return boto3.client(**s3_params)

def upload_file_to_s3(file_name, bucket, object_name=None):
    """
    S3にファイルをアップロードする関数
    
    Args:
        file_name (str): アップロードするファイルのパス
        bucket (str): アップロード先のS3バケット名
        object_name (str): アップロードするオブジェクト名 (省略可)
        
    Returns:
        dict: アップロード結果 (成功時はオブジェクト名、失敗時はNone)
    """
    
    s3_client = get_s3_client()
    
    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f'{object_name} uploaded to {bucket} successfully.')
        return {"key": object_name}
    except Exception as e:
        print(f'File upload failed: {str(e)}')
        raise

def download_file_from_s3(bucket, object_name, file_name):
    """
    S3からファイルをダウンロードする関数
    
    Args:
        bucket (str): ダウンロード元のS3バケット名
        object_name (str): ダウンロードするオブジェクト名
        file_name (str): ダウンロード後のファイル名
        
    Returns:
        str: ダウンロード結果メッセージ
    """
    
    s3_client = get_s3_client()
    
    try:
        s3_client.download_file(bucket, object_name, file_name)
        return f'{object_name} downloaded from {bucket} to {file_name}.'
    except Exception as e:
        return f'File download failed: {str(e)}'

def check_file_exists_in_s3(bucket, object_name):
    """
    S3上にファイルが存在するか確認する関数
    
    Args:
        bucket (str): チェックするS3バケット名
        object_name (str): チェックするオブジェクト名
        
    Returns:
        dict: チェック結果 (存在する場合はオブジェクト名、存在しない場合はNone)
    """
    
    s3_client = get_s3_client()
    
    try:
        s3_client.head_object(Bucket=bucket, Key=object_name)
        return {"key": object_name}
    except s3_client.exceptions.ClientError as e:
        # ファイルが存在しない場合のエラーコードに基づいてFalseを返す
        if e.response['Error']['Code'] == '404':
            return {"key": None}
        else:
            print(f'File check failed: {str(e)}')
            raise

def list_files_in_s3(bucket, prefix=""):
    """
    S3上のオブジェクト一覧を取得する関数
    
    Args:
        bucket (str): リスト取得するS3バケット名
        prefix (str): リスト取得するオブジェクトのプレフィックス (省略可)
        
    Returns:
        list: オブジェクト一覧 (存在しない場合は空リスト)
    """
    
    s3_client = get_s3_client()

    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' in response:
            return [{
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"].strftime('%Y-%m-%d %H:%M:%S')
            } for obj in response['Contents']]
        else:
            return []
    except Exception as e:
        return f'Listing files failed: {str(e)}'

def delete_file_from_s3(bucket, object_name):
    """
    S3上のオブジェクトを削除する関数
    
    Args:
        bucket (str): 削除するS3バケット名
        object_name (str): 削除するオブジェクト名
        
    Returns:
        str: 削除結果メッセージ
    """
    
    s3_client = get_s3_client()

    try:
        s3_client.delete_object(Bucket=bucket, Key=object_name)
        return {"key": object_name}
    except Exception as e:
        print(f'File deletion failed: {str(e)}')
        
