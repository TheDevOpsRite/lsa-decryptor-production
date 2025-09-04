from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from io import BytesIO
import filetype
from decryptor import decrypt_file, decrypt_file_header, decrypt_bytes, decrypt_header_bytes

app = FastAPI()

# Configure CORS origins from environment for flexibility in Render/Vercel deployments.
# Set ALLOWED_ORIGINS to a comma-separated list (e.g. https://example.com,https://other.com)
env_origins = os.getenv('ALLOWED_ORIGINS', '')
if env_origins:
    allow_origins = [o.strip() for o in env_origins.split(',') if o.strip()]
else:
    # Fallback: allow all origins during initial testing; tighten this in production.
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose Content-Disposition and X-Filename so browsers running the frontend can
    # read the server-provided filename instead of guessing/forcing an extension.
    expose_headers=["Content-Disposition", "X-Filename"],
)


@app.get('/health')
def health():
    return {"status": "ok"}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB max file size to accept 
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
        # .lsa files are images — decrypt entire payload
        data = decrypt_bytes(contents)
    elif ext == 'lsav':
        # .lsav files are videos — decrypt the full file so the resulting
        # output is a valid MP4 rather than a corrupted image-like blob.
        data = decrypt_bytes(contents)
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    # If the uploaded file was .lsav we expect a video (mp4) after header decryption
    if ext == 'lsav':
        out_ext = 'mp4'
        mime = 'video/mp4'
    else:
        # Robust file type detection: prefer filetype.guess, then fall back to common header checks
        kind = filetype.guess(data)
        if kind:
            out_ext = kind.extension
            mime = kind.mime
        else:
            head = data[:4096]
            if head.startswith(b'\xff\xd8\xff'):
                out_ext = 'jpg'
                mime = 'image/jpeg'
            elif head.startswith(b'\x89PNG\r\n\x1a\n'):
                out_ext = 'png'
                mime = 'image/png'
            elif b'ftyp' in head[:4096]:
                # MP4 / ISO Base Media
                out_ext = 'mp4'
                mime = 'video/mp4'
            elif head.startswith(b'\x1A\x45\xDF\xA3'):
                out_ext = 'mkv'
                mime = 'video/x-matroska'
            else:
                out_ext = 'bin'
                mime = 'application/octet-stream'

    out_name = filename.rsplit('.', 1)[0] + f'.{out_ext}'
    # Quote the filename to be safe for spaces and special characters and add
    # an X-Filename header to make it easy for the frontend to read the value.
    content_disposition = f'attachment; filename="{out_name}"'
    buf = BytesIO(data)
    buf.seek(0)
    return StreamingResponse(buf, media_type=mime, headers={
        "Content-Disposition": content_disposition,
        "X-Filename": out_name
    })

@app.get('/')
def home():
    return {"message": "MIUI LSA Decryptor FastAPI Backend Running"}
