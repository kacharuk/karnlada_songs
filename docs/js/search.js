// Search functionality for index page

function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearch');
    const albumSections = document.querySelectorAll('.album-section');

    if (!searchInput) return;

    // Search function
    function performSearch() {
        const query = searchInput.value.toLowerCase().trim();

        if (!query) {
            // Show all songs and albums
            albumSections.forEach(section => {
                section.style.display = 'block';
                const songs = section.querySelectorAll('.song-item');
                songs.forEach(song => song.style.display = 'flex');
            });
            if (clearSearchBtn) clearSearchBtn.style.display = 'none';
            return;
        }

        if (clearSearchBtn) clearSearchBtn.style.display = 'inline-block';

        let hasResults = false;

        albumSections.forEach(section => {
            const songs = section.querySelectorAll('.song-item');
            let albumHasVisibleSongs = false;

            songs.forEach(song => {
                const title = song.querySelector('.song-title').textContent.toLowerCase();
                const matches = title.includes(query);

                if (matches) {
                    song.style.display = 'flex';
                    albumHasVisibleSongs = true;
                    hasResults = true;
                } else {
                    song.style.display = 'none';
                }
            });

            // Show/hide album section based on whether it has visible songs
            section.style.display = albumHasVisibleSongs ? 'block' : 'none';
        });

        // Show "no results" message if needed
        let noResultsMsg = document.getElementById('noResultsMessage');
        if (!hasResults) {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.id = 'noResultsMessage';
                noResultsMsg.style.cssText = `
                    text-align: center;
                    padding: 40px;
                    color: white;
                    font-size: 18px;
                `;
                noResultsMsg.textContent = `ไม่พบเพลง "${searchInput.value}"`;
                document.querySelector('.container').appendChild(noResultsMsg);
            } else {
                noResultsMsg.textContent = `ไม่พบเพลง "${searchInput.value}"`;
                noResultsMsg.style.display = 'block';
            }
        } else if (noResultsMsg) {
            noResultsMsg.style.display = 'none';
        }
    }

    // Clear search
    function clearSearch() {
        searchInput.value = '';
        performSearch();
        searchInput.focus();
    }

    // Event listeners
    searchInput.addEventListener('input', performSearch);
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', clearSearch);
    }

    // Enter key to focus first result
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const firstVisibleSong = document.querySelector('.song-item[style*="display: flex"], .song-item:not([style*="display: none"])');
            if (firstVisibleSong) {
                const playButton = firstVisibleSong.querySelector('.play-button');
                if (playButton) playButton.click();
            }
        }
    });
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSearch);
} else {
    initializeSearch();
}
