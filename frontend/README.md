# MIUI LSA/LSAV Decryptor Frontend

This is a simple HTML/CSS/JS frontend for uploading and (simulated) decrypting MIUI LSA/LSAV files. Actual decryption must be performed server-side or with WASM.

## Features
- Upload multiple `.lsa` or `.lsav` files
- Simulated decryption and download of output files
- Download all decrypted files at once

## Usage
1. Open `index.html` in your browser.
2. Select one or more `.lsa` or `.lsav` files.
3. Click "Decrypt & Download" to simulate decryption and download output files.
4. Use "Download All" to download all files at once.

## Note
This demo does not perform real decryption. For actual decryption, integrate with your Python backend or use WASM.
