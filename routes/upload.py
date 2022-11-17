import sys
import shutil
import aiofiles
from fastapi import APIRouter, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
from PIL import Image
from modules.TOOLS import getUUID
from config import settings
sys.path.append('..')
router = APIRouter()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


def allowed_file_mime_type(content_type):
    return content_type in settings.ALLOWED_EXTENSIONS_MIME_TYPES


@router.post("/", tags=['UPLOAD'], summary="上傳資料")
async def upload_file(request: Request, files: List[UploadFile]):
    filenames = []
    for file in files:
        # 基礎驗證

        if not file:
            raise HTTPException(status_code=401, detail='不被允許的檔案類型1')
        if file.filename == '':
            raise HTTPException(status_code=401, detail='不被允許的檔案類型2')
        if not allowed_file(file.filename):
            raise HTTPException(status_code=401, detail='不被允許的檔案類型3')
        print(file)
        if not allowed_file_mime_type(file.content_type):
            raise HTTPException(status_code=401, detail='是不被允許的檔案類型4')
        # 存入資料夾
        uuid = getUUID()
        async with aiofiles.open(settings.UPLOAD_FOLDER + uuid, 'wb') as out_file:
            content = await file.read()  # async read
            if len(content) >= settings.MAX_UPLOAD_SIZE:
                raise HTTPException(status_code=401, detail='檔案不得超過5MB')
            # 依類型不同存入
            if file.filename in ['jpeg', 'png', 'jpg']:
                webpimg = Image.open(content)
                webpimg.save(uuid, format='webp')
            else:
                await out_file.write(content)  # async write
            filenames.append(uuid)
    return filenames


@router.get("/", tags=['UPLOAD'], summary='測試上傳')
async def main():
    content = """
        <form action="/upload/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)