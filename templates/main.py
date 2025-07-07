import os
import shutil

from fastapi import FastAPI, UploadFile, File
import uvicorn


app = FastAPI()


# IF TO USE ONE BYTES READ FOR FILE - IT WILL BE EXPIRED
# YOU CANNOT USE SEVERAL FILE CONTENT READS
# YOU CANNOT SEND JSON WITH FILES


@app.post('/files')
async def upload_file(file: UploadFile = File()):
    os.makedirs("temporary_files", exist_ok=True)
    
    with open(f"temporary_files/{file.filename}", mode="wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "name": file,
        "name2": file.filename,
        "type": file.content_type,
        "size": file.size
    }
    
    
@app.post('/files/validate')
async def upload_validated_file(file: UploadFile = File()):
    file_content = await file.read()
    LIMIT_SIZE = 1024 * 1024
    if len(file_content) > LIMIT_SIZE or not file.content_type.startswith("text/"):
        return {
            "message": "GAY"
        }
    text = file_content.decode("utf-8")
    amount_of_symbols = len(text)
    return {
        "content_size": len(file_content),
        "symbols_amount": amount_of_symbols,
        "lines_amount": len(text.splitlines())
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
