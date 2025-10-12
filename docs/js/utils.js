// Utility functions for Karnlada Songs
// Shared across index and player pages

// Generate QR code URL using a free QR code API
function generateQRCodeUrl(url) {
    // Using QR Server API (free, no registration needed)
    const size = 300;
    const encodedUrl = encodeURIComponent(url);
    return `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodedUrl}`;
}

// Show QR code in a modal
function showQRCodeModal(url, title) {
    // Remove existing modal if any
    const existingModal = document.getElementById('qrModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Create modal
    const modal = document.createElement('div');
    modal.id = 'qrModal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;

    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background: white;
        border-radius: 16px;
        padding: 30px;
        max-width: 400px;
        text-align: center;
        position: relative;
    `;

    modalContent.innerHTML = `
        <button id="closeQRModal" style="
            position: absolute;
            top: 10px;
            right: 10px;
            background: #f56565;
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 18px;
            line-height: 1;
        ">×</button>
        <h2 style="color: #2d3748; margin-bottom: 15px; font-size: 20px;">${escapeHtml(title)}</h2>
        <img src="${generateQRCodeUrl(url)}" alt="QR Code" style="width: 100%; max-width: 300px; border-radius: 8px;">
        <p style="color: #718096; margin-top: 15px; font-size: 14px; word-break: break-all;">${escapeHtml(url)}</p>
    `;

    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Close modal on click outside or close button
    modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.id === 'closeQRModal') {
            modal.remove();
        }
    });
}

// Share a song link
async function shareSong(url, title, artist) {
    const shareData = {
        title: title,
        text: `Listen to "${title}" by ${artist}`,
        url: url
    };

    // Check if Web Share API is supported
    if (navigator.share) {
        try {
            await navigator.share(shareData);
            return { success: true, method: 'native' };
        } catch (err) {
            if (err.name === 'AbortError') {
                return { success: false, error: 'Share cancelled' };
            }
            // Fall through to clipboard copy
        }
    }

    // Fallback: copy URL to clipboard
    if (navigator.clipboard) {
        try {
            await navigator.clipboard.writeText(url);
            return { success: true, method: 'clipboard' };
        } catch (err) {
            return { success: false, error: 'Could not copy to clipboard' };
        }
    }

    return { success: false, error: 'Sharing not supported' };
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Get base URL for sharing
function getBaseUrl() {
    return 'https://kacharuk.github.io/karnlada_songs';
}

// Build share URL for a song
function getSongShareUrl(songId) {
    return `${getBaseUrl()}/songs/${songId}.html`;
}

// Build playlist URL
function getPlaylistUrl(songIds) {
    return `${getBaseUrl()}/player.html?ids=${songIds.join(',')}`;
}

// Format time in mm:ss
function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}
