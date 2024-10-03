import os

from fastapi import APIRouter, Query, File, UploadFile, HTTPException

from ..config import AWS_S3_BUCKET_NAME
from ..utils.s3_helper import (
    upload_file_to_s3,
    download_file_from_s3,
    delete_file_from_s3,
    list_files_in_s3
)

router = APIRouter()

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    """
    S3 にファイルをアップロードするエンドポイント
    
    Args:
        file (UploadFile): アップロードするファイル
    
    Returns:
        dict: アップロード結果メッセージ
    """
    print(f'Uploading file: {file.filename}')
    status = 'success'
    try:
        file_location = f'/tmp/{file.filename}' 

        with open(file_location, 'wb') as buffer:
            buffer.write(await file.read())

        result = upload_file_to_s3(file_location, AWS_S3_BUCKET_NAME)

        os.remove(file_location)

        return result
    except Exception as e:
        print(e)
        status = 'failed'
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/download/{file_name}')
async def download_file(file_name: str):
    """
    S3 からファイルをダウンロードするエンドポイント
    """
    try:
        file_location = f'/tmp/{file_name}'

        result = download_file_from_s3(AWS_S3_BUCKET_NAME, file_name, file_location)

        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete')
async def delete_file(file_name: str = Query(..., description='削除するファイル名')):
    """
    S3 からファイルを削除するエンドポイント
    """
    if not file_name:
        raise HTTPException(status_code=400, detail='ファイル名を指定してください')
    try:
        result = delete_file_from_s3(AWS_S3_BUCKET_NAME, file_name)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/files')
async def list_files(prefix: str = ''):
    """
    S3 のファイル一覧を取得するエンドポイント
    """
    try:
        files = list_files_in_s3(AWS_S3_BUCKET_NAME, prefix)
        print(len(files))
        return {'files': files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))