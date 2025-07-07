import uuid
import io
import shutil

from PIL import Image

from fastapi import FastAPI, UploadFile, File, HTTPException, status, Path
from fastapi.responses import FileResponse


app = FastAPI()


IMAGE_TYPES = [
    "image/png",
    "image/jpg"
]
MAX_SIZE = 1024 * 1024 * 5


DATABASE = [
    
]


@app.post("/photos/upload")
async def photos_upload_hand(file: UploadFile = File(...)):
    file_content_type = file.content_type
    print(file_content_type)
    if file_content_type not in IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File content type is invalid"
        )
    if file.size > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File size is invalid"
        )    
    try:
        file_content = await file.read()
        image = Image.open(io.BytesIO(file_content))
        image.verify()
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File is invalid"
        )
    file_name = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1]
    full_file_name = file_name + '.' + file_extension
    with open(f'temporary/{full_file_name}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    DATABASE.append({
        "filename": full_file_name,
        "content_type": file.content_type
    })
    return file
    


@app.get('/photos/list')
async def photos_list_hand():
    data = {
        "data": DATABASE
    }
    return data


@app.get('/photos/{filename}')
async def photos_filename_hand(filename: str = Path(...)):
    file = None
    for f in DATABASE:
        if f["filename"] == filename:
            file = f
            break
    if not file:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File was not found"
        )
    response = FileResponse(
        path=f'temporary/{file["filename"]}',
        media_type=file["content_type"]
    )
    return response
