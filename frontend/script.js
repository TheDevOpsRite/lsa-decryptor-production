// Minimal frontend for MIUI LSA Decryptor
// Select a file, send to FastAPI backend, receive decrypted image, show download link

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const resultDiv = document.getElementById('result');
    const decryptBtn = document.getElementById('decryptBtn');
    const overlay = document.getElementById('loadingOverlay');
    const loadingVideo = document.getElementById('loadingVideo');
    const loadingMessage = document.getElementById('loadingMessage');

    decryptBtn.addEventListener('click', async function(event) {
        event.preventDefault(); // Prevent form submission
        console.log('Decrypt button clicked, event handler triggered.');
        event.stopPropagation(); // Stop the event from propagating further
        console.log('Event propagation stopped.');

        resultDiv.innerHTML = '';        
        const file = fileInput.files[0];
        if (!file) {
            resultDiv.innerHTML = '<p>Please select a .lsa or .lsav file.</p>';
            return;
        }
        const formData = new FormData();
        formData.append('file', file);
        // Show loading overlay and play animation/video while decrypting
        try {
            if (overlay) overlay.style.display = 'flex';
            if (loadingMessage) loadingMessage.style.display = 'block';
            if (loadingVideo) {
                try { loadingVideo.play(); } catch (e) { /* ignore */ }
            }
        } catch (e) { /* ignore UI errors */ }
        // Prevent repeated clicks while processing
        decryptBtn.disabled = true;
    try {
                // Determine backend base URL: prefer meta tag, then environment, then fallback
                const metaApi = document.querySelector('meta[name="api-base"]')?.getAttribute('content') || '';
                const envBase = ''; // placeholder if you want to inject at build time
                const fallback = 'https://lsa-decryptor-production.onrender.com';
                const base = (metaApi && metaApi.trim()) ? metaApi.trim() : (envBase || fallback);
                const response = await fetch(`${base}/api/decrypt`, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                let errorMsg = 'Unknown error';
                try {
                    const error = await response.json();
                    errorMsg = error.error || errorMsg;
                } catch {}
                resultDiv.innerHTML = `<p>Error decrypting ${file.name}: ${errorMsg}</p>`;
                return;
            }
            const blob = await response.blob();
            // Determine output filename: prefer server-provided Content-Disposition
            // filename. If missing, infer from Content-Type / blob.type. Avoid
            // defaulting to .jpg which caused videos to be saved as images.
            let outName = file.name.replace(/\.(lsa|lsav)$/i, '');
            // Prefer X-Filename header (added by server) which is easier to parse.
            const xname = response.headers.get('X-Filename');
            if (xname) {
                outName = xname;
            } else {
                const disp = response.headers.get('Content-Disposition');
                if (disp) {
                    const match = disp.match(/filename="?([^";]+)"?/);
                    if (match) outName = match[1];
                } else {
                // No filename header; use Content-Type / blob.type to pick an extension
                const ct = response.headers.get('Content-Type') || '';
                let ext = '';
                if (ct.includes('video')) ext = '.mp4';
                else if (ct.includes('jpeg') || ct.includes('jpg')) ext = '.jpg';
                else if (ct.includes('png')) ext = '.png';
                else if (ct.includes('mpeg')) ext = '.mp4';
                else if (blob && blob.type) {
                    if (blob.type.includes('video')) ext = '.mp4';
                    else if (blob.type.includes('jpeg')) ext = '.jpg';
                    else if (blob.type.includes('png')) ext = '.png';
                }
                outName = outName + (ext || '.bin');
                }
            }
            // If the uploaded file was a .lsav and we still don't have a proper
            // video extension, force .mp4 so the decrypted video is saved correctly.
            const inputExt = (file.name.match(/\.([^.]+)$/) || [])[1] || '';
            if (/lsav/i.test(inputExt)) {
                // If outName doesn't already end with a known video ext, replace/fix it
                if (!/\.(mp4|mkv|mov|webm)$/i.test(outName)) {
                    // Keep base name and force .mp4
                    const base = outName.replace(/\.[^.]+$/, '');
                    outName = base + '.mp4';
                }
            }
            // Auto-download the decrypted file
            const objectUrl = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = objectUrl;
            link.download = outName;
            document.body.appendChild(link);
            link.click();
            link.remove();
            // Keep a small download link for fallback
            const dl = document.createElement('a');
            dl.href = objectUrl;
            dl.download = outName;
            dl.textContent = `Download ${outName}`;
            dl.className = 'download-link';
            resultDiv.appendChild(dl);
            // Hide loading overlay and restore UI
            try {
                if (overlay) overlay.style.display = 'none';
                if (loadingVideo) { try { loadingVideo.pause(); loadingVideo.currentTime = 0; } catch (e) {} }
            } catch (e) {}
            decryptBtn.disabled = false;
        } catch (err) {
            resultDiv.innerHTML = `<p>Error decrypting ${file.name}: ${err}</p>`;            
            // Hide loading overlay and restore UI on error
            try {
                if (overlay) overlay.style.display = 'none';
                if (loadingVideo) { try { loadingVideo.pause(); loadingVideo.currentTime = 0; } catch (e) {} }
            } catch (e) {}
            decryptBtn.disabled = false;
        }
        return false; // Explicitly prevent any default action or propagation
    });
});
