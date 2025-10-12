// Enhanced player with playlist support

let playlist = [];
let allFiles = [];
let currentIndex = 0;
let currentFile = null;
let nextAudioPreload = null;

async function fetchJSON(path) {
    try {
        const r = await fetch(path);
        if (!r.ok) throw new Error('Fetch failed');
        return await r.json();
    } catch (e) {
        console.error(e);
        return null;
    }
}

function getQueryParam(name) {
    const params = new URLSearchParams(location.search);
    return params.get(name);
}

function setStatus(text, cls = '') {
    const s = document.getElementById('status');
    if (s) {
        s.textContent = text;
        s.className = 'status' + (cls ? ' ' + cls : '');
    }
}

function selectFile(files, id) {
    if (!id) return files[0];
    // First try matching by song_id (stable ID)
    for (const f of files) {
        if (f.song_id === id) return f;
    }
    // if id is numeric index
    if (/^\d+$/.test(id)) {
        const idx = parseInt(id, 10) - 1;
        return files[idx] || files[0];
    }
    // try matching by filename or title (backward compatibility)
    for (const f of files) {
        if (f.html_filename === id || f.html_filename.replace('.html', '') === id) return f;
        if (f.title === id) return f;
    }
    return files[0];
}

function togglePlayPause() {
    const audioEl = document.getElementById('audioPlayer');
    if (audioEl.paused) {
        audioEl.play();
    } else {
        audioEl.pause();
    }
}

function updatePlayPauseButton() {
    const audioEl = document.getElementById('audioPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const playBtn = document.getElementById('playBtn');

    if (audioEl.paused) {
        playPauseBtn.classList.remove('playing');
        playBtn.textContent = '▶ Play';
    } else {
        playPauseBtn.classList.add('playing');
        playBtn.textContent = '⏸ Pause';
    }
}

async function shareCurrentSong() {
    if (!currentFile) return;

    const shareUrl = getSongShareUrl(currentFile.html_filename.replace('.html', ''));
    const result = await shareSong(shareUrl, currentFile.title, currentFile.artist);

    if (result.success) {
        if (result.method === 'native') {
            setStatus('Shared successfully!', 'playing');
        } else {
            setStatus('Link copied to clipboard!', 'playing');
        }
    } else {
        setStatus(result.error || 'Could not share', 'error');
    }
}

function loadSong(index) {
    if (index < 0 || index >= playlist.length) {
        setStatus('End of playlist', '');
        return;
    }

    const file = playlist[index];

    // Skip external links
    if (file.is_external) {
        setStatus(`Skipping external link: ${file.title}`, 'error');
        setTimeout(() => {
            loadSong(index + 1);
        }, 1000);
        return;
    }

    currentIndex = index;
    currentFile = file;

    // Update UI
    document.getElementById('songTitle').textContent = file.title;
    document.getElementById('artistName').textContent = file.artist;
    const art = document.getElementById('albumArt');
    art.src = file.album_art_url || 'images/album_art_karnlada.jpg';
    art.alt = file.title + ' album art';

    // Load audio
    const audioEl = document.getElementById('audioPlayer');
    // Clear existing sources
    while (audioEl.firstChild) audioEl.removeChild(audioEl.firstChild);
    const src = document.createElement('source');
    src.src = file.audio_url;
    src.type = 'audio/mpeg';
    audioEl.appendChild(src);
    const src2 = document.createElement('source');
    src2.src = file.audio_url;
    src2.type = 'audio/mp4';
    audioEl.appendChild(src2);
    audioEl.load();

    // Update next song info
    updateNextSongInfo();

    // Update playlist UI
    updatePlaylistUI();

    // Cancel any existing preload
    if (nextAudioPreload) {
        nextAudioPreload.src = '';
        nextAudioPreload = null;
    }
}

function updateNextSongInfo() {
    const nextSongEl = document.getElementById('nextSong');
    if (!nextSongEl) return;

    // Find next non-external song
    let nextIndex = currentIndex + 1;
    let nextSong = null;

    while (nextIndex < playlist.length) {
        if (!playlist[nextIndex].is_external) {
            nextSong = playlist[nextIndex];
            break;
        }
        nextIndex++;
    }

    if (nextSong) {
        nextSongEl.textContent = `Next: ${nextSong.title}`;
        nextSongEl.style.display = 'block';
    } else {
        nextSongEl.textContent = 'Last song in playlist';
        nextSongEl.style.display = 'block';
    }
}

function playNextSong() {
    loadSong(currentIndex + 1);
    const audioEl = document.getElementById('audioPlayer');
    audioEl.play().catch(e => {
        console.error('Autoplay failed:', e);
        setStatus('Click play to continue', '');
    });
}

function preloadNextSong() {
    // Find next non-external song
    let nextIndex = currentIndex + 1;
    while (nextIndex < playlist.length) {
        if (!playlist[nextIndex].is_external) {
            const nextFile = playlist[nextIndex];
            if (nextFile && !nextAudioPreload) {
                nextAudioPreload = new Audio(nextFile.audio_url);
                nextAudioPreload.preload = 'auto';
                console.log('Preloading next song:', nextFile.title);
            }
            break;
        }
        nextIndex++;
    }
}

function updatePlaylistUI() {
    const playlistContainer = document.getElementById('playlistContainer');
    if (!playlistContainer || playlist.length <= 1) {
        if (playlistContainer) playlistContainer.style.display = 'none';
        return;
    }

    playlistContainer.style.display = 'block';
    const playlistEl = document.getElementById('playlistSongs');
    playlistEl.innerHTML = '';

    playlist.forEach((song, index) => {
        const songItem = document.createElement('div');
        songItem.className = 'playlist-song-item';
        if (index === currentIndex) {
            songItem.classList.add('playing');
        }
        if (song.is_external) {
            songItem.classList.add('external');
        }

        const songInfo = document.createElement('div');
        songInfo.className = 'playlist-song-info';

        const indicator = document.createElement('span');
        indicator.className = 'playlist-indicator';
        indicator.textContent = index === currentIndex ? '▶' : (index + 1);

        const title = document.createElement('span');
        title.className = 'playlist-song-title';
        title.textContent = song.title;
        if (song.is_external) {
            title.textContent += ' [external link]';
        }

        songInfo.appendChild(indicator);
        songInfo.appendChild(title);
        songItem.appendChild(songInfo);

        if (!song.is_external) {
            songItem.style.cursor = 'pointer';
            songItem.addEventListener('click', () => {
                loadSong(index);
                document.getElementById('audioPlayer').play();
            });
        }

        playlistEl.appendChild(songItem);
    });
}

async function initPlayer() {
    const filesData = await fetchJSON('onedrive_files.json');
    if (!filesData || !filesData.files || filesData.files.length === 0) {
        setStatus('No files found', 'error');
        return;
    }

    allFiles = filesData.files;

    // Get song IDs from URL
    const idsParam = getQueryParam('ids');
    const singleId = getQueryParam('id');

    if (idsParam) {
        // Playlist mode
        const ids = idsParam.split(',');
        playlist = ids.map(id => selectFile(allFiles, id)).filter(f => f);
    } else if (singleId) {
        // Single song mode
        const file = selectFile(allFiles, singleId);
        if (file) {
            playlist = [file];
        }
    } else {
        // Default to first song
        playlist = [allFiles[0]];
    }

    if (playlist.length === 0) {
        setStatus('No songs to play', 'error');
        return;
    }

    // Setup audio element event listeners
    const audioEl = document.getElementById('audioPlayer');

    audioEl.addEventListener('loadstart', () => setStatus('Loading audio...', 'loading'));
    audioEl.addEventListener('canplay', () => setStatus('Ready to play'));
    audioEl.addEventListener('playing', () => {
        setStatus('Now playing', 'playing');
        updatePlayPauseButton();
    });
    audioEl.addEventListener('pause', () => {
        setStatus('Paused');
        updatePlayPauseButton();
    });
    audioEl.addEventListener('ended', () => {
        setStatus('Song ended');
        updatePlayPauseButton();
        playNextSong();
    });
    audioEl.addEventListener('error', () => setStatus('Error loading audio', 'error'));

    audioEl.addEventListener('loadedmetadata', () => {
        const durationEl = document.getElementById('duration');
        if (durationEl) {
            durationEl.textContent = formatTime(audioEl.duration);
        }
    });

    audioEl.addEventListener('timeupdate', () => {
        const timeSlider = document.getElementById('timeSlider');
        const currentTimeEl = document.getElementById('currentTime');

        if (timeSlider && !timeSlider.dataset.seeking) {
            const percent = (audioEl.currentTime / audioEl.duration) * 100;
            timeSlider.value = percent || 0;
        }

        if (currentTimeEl) {
            currentTimeEl.textContent = formatTime(audioEl.currentTime);
        }

        // Preload next song in last 15 seconds
        if (audioEl.duration - audioEl.currentTime <= 15 && !nextAudioPreload) {
            preloadNextSong();
        }
    });

    // Setup control bindings
    const playPauseBtn = document.getElementById('playPauseBtn');
    const playBtn = document.getElementById('playBtn');
    const shareBtn = document.getElementById('shareBtn');
    const albumWrapper = document.getElementById('albumWrapper');
    const timeSlider = document.getElementById('timeSlider');

    if (playPauseBtn) {
        playPauseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            togglePlayPause();
        });
    }

    if (playBtn) {
        playBtn.addEventListener('click', togglePlayPause);
    }

    if (albumWrapper) {
        albumWrapper.addEventListener('click', togglePlayPause);
    }

    if (shareBtn) {
        shareBtn.addEventListener('click', shareCurrentSong);
    }

    // Time slider
    if (timeSlider) {
        timeSlider.addEventListener('input', () => {
            timeSlider.dataset.seeking = 'true';
            const time = (timeSlider.value / 100) * audioEl.duration;
            const currentTimeEl = document.getElementById('currentTime');
            if (currentTimeEl) {
                currentTimeEl.textContent = formatTime(time);
            }
        });

        timeSlider.addEventListener('change', () => {
            const time = (timeSlider.value / 100) * audioEl.duration;
            audioEl.currentTime = time;
            delete timeSlider.dataset.seeking;
        });
    }

    // Load first song
    loadSong(0);

    // Try to autoplay if allowed
    try {
        await audioEl.play();
    } catch (e) {
        setStatus('Click play to start');
    }
}

// Initialize player
initPlayer();
