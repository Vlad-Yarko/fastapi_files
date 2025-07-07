import io

from PIL import Image

import shutil
import tempfile
from typing import Any

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends


app = FastAPI()

# File = Form, Query, Path

@app.post("/")
async def upload_file(file: UploadFile = File()):
    import os
    os.makedirs("temp", exist_ok=True)

    with open(f"temp/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "name": file.file,
        "name2": file.filename,
        "type": file.content_type,
        "size": file.size
    }


@app.post("/upload-small-file/")
async def upload_small_file(file: UploadFile = File(...)):
    if not file.content_type.startswith("text/"):
        return {"error": "Файл повинен бути текстовим"}

    content = await file.read()

    text = content.decode("utf-8")
    line_count = len(text.splitlines())
    return line_count

LIMIT_SIZE = 1024 * 1024 * 2

LIST_OF_AVAILABLE_TYPE_OF_IMAGE = (
    "image/png",
    "image/jpg",
    "image/jpeg"
)

async def validate_file(file: UploadFile = File(...)) -> dict[str, Any]:
    # if not file.content_type.startswith("image/"):
    #     raise HTTPException(422, "File is not image")

    if file.content_type not in LIST_OF_AVAILABLE_TYPE_OF_IMAGE:
        raise HTTPException(422, "File is not image")

    if file.size > LIMIT_SIZE:
        raise HTTPException(422, "File big")

    try:
        file_content = await file.read()
        image = Image.open(io.BytesIO(file_content))
        image.verify()
        return {
            "name": file.file,
            "name2": file.filename,
            "type": file.content_type,
            "size": file.size
        }
    except:
        raise HTTPException(422, "Bad file")


@app.post("/upload-small-file2/")
async def upload_small_file(file = Depends(validate_file)):
    return file
