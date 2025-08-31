from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from io import BytesIO
import filetype
from decryptor import decrypt_file, decrypt_file_header, decrypt_bytes, decrypt_header_bytes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lsadecryptor.vercel.app/" , "http://127.0.0.1:5500/frontend/index.html" , "http://127.0.0.1:5500"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {'lsa', 'lsav'}

@app.post('/api/decrypt')
async def decrypt(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JSONResponse(status_code=400, content={"error": "Invalid file type"})
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        return JSONResponse(status_code=400, content={"error": "File too large"})
    # Decrypt in-memory without writing to disk
    if ext == 'lsa':
        data = decrypt_bytes(contents)
    elif ext == 'lsav':
        data = decrypt_header_bytes(contents)
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    out_ext = filetype.guess_extension(data[:1024]) or 'jpg'
    out_name = filename.rsplit('.', 1)[0] + f'.{out_ext}'
    # Check JPEG header
    if out_ext == 'jpg' and data[:3] != b'\xff\xd8\xff':
        return JSONResponse(status_code=400, content={"error": "Decrypted file is not a valid JPEG image."})

    img_io = BytesIO(data)
    img_io.seek(0)
    return StreamingResponse(img_io, media_type=f'image/{out_ext}', headers={
        "Content-Disposition": f"attachment; filename={out_name}"
    })

@app.get('/')
def home():
    return {"message": "MIUI LSA Decryptor FastAPI Backend Running"}
