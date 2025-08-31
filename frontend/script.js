// Minimal frontend for MIUI LSA Decryptor
// Select a file, send to FastAPI backend, receive decrypted image, show download link

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const resultDiv = document.getElementById('result');
    const decryptBtn = document.getElementById('decryptBtn');

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
            let outName = file.name.replace(/\.(lsa|lsav)$/i, '.jpg');
            const disp = response.headers.get('Content-Disposition');
            if (disp) {
                const match = disp.match(/filename="?([^";]+)"?/);
                if (match) outName = match[1];
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
        } catch (err) {
            resultDiv.innerHTML = `<p>Error decrypting ${file.name}: ${err}</p>`;            
        }
        return false; // Explicitly prevent any default action or propagation
    });
});
