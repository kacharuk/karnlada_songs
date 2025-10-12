#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate HTML music player files from OneDrive file list.
Each HTML includes Open Graph metadata for proper preview in Messenger.
"""

import json
import os
import sys
from html import escape
import hashlib

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def generate_html_player(file_info, base_url):
    """
    Generate an HTML music player with:
    - Auto-play functionality
    - Album art display
    - Open Graph meta tags for social sharing (Messenger preview)
    - Responsive design
    """

    title = escape(file_info['title'])
    artist = escape(file_info['artist'])
    audio_url = escape(file_info['audio_url'])
    album_art_url = escape(file_info['album_art_url'])
    html_filename = file_info['html_filename']

    # Generate the full GitHub Pages URL for this HTML file
    page_url = f"{base_url}/{html_filename}"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {artist}</title>

    <!-- Open Graph meta tags for Messenger and social media preview -->
    <meta property="og:type" content="music.song">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="Artist: {artist}">
    <meta property="og:image" content="{album_art_url}">
    <meta property="og:url" content="{page_url}">
    <meta property="og:audio" content="{audio_url}">
    <meta property="music:musician" content="{artist}">

    <!-- Twitter Card meta tags -->
    <meta name="twitter:card" content="player">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="Artist: {artist}">
    <meta name="twitter:image" content="{album_art_url}">

    <!-- Additional meta tags -->
    <meta name="description" content="{title} by {artist}">
    <meta name="author" content="{artist}">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .player-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}

        .album-art {{
            width: 100%;
            aspect-ratio: 1;
            object-fit: cover;
            display: block;
        }}

        .player-info {{
            padding: 30px;
            text-align: center;
        }}

        .song-title {{
            font-size: 24px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 8px;
            line-height: 1.3;
        }}

        .artist-name {{
            font-size: 18px;
            color: #718096;
            margin-bottom: 25px;
        }}

        .audio-controls {{
            width: 100%;
            margin-top: 20px;
            outline: none;
        }}

        /* Custom audio player styling */
        audio {{
            width: 100%;
            height: 40px;
            border-radius: 20px;
        }}

        audio::-webkit-media-controls-panel {{
            background-color: #f7fafc;
            border-radius: 20px;
        }}

        .status {{
            margin-top: 15px;
            font-size: 14px;
            color: #a0aec0;
            font-style: italic;
        }}

        .loading {{
            color: #667eea;
        }}

        .playing {{
            color: #48bb78;
        }}

        .error {{
            color: #f56565;
        }}

        @media (max-width: 480px) {{
            .song-title {{
                font-size: 20px;
            }}

            .artist-name {{
                font-size: 16px;
            }}

            .player-info {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="player-container">
        <img src="{album_art_url}" alt="{title} album art" class="album-art" id="albumArt">

        <div class="player-info">
            <h1 class="song-title">{title}</h1>
            <p class="artist-name">{artist}</p>

            <audio id="audioPlayer" class="audio-controls" controls>
                <source src="{audio_url}" type="audio/mpeg">
                <source src="{audio_url}" type="audio/mp4">
                Your browser does not support the audio element.
            </audio>

            <div class="status" id="status">Loading...</div>
        </div>
    </div>

    <script>
        const audio = document.getElementById('audioPlayer');
        const status = document.getElementById('status');
        const albumArt = document.getElementById('albumArt');

        // Update status based on audio events
        audio.addEventListener('loadstart', () => {{
            status.textContent = 'Loading audio...';
            status.className = 'status loading';
        }});

        audio.addEventListener('canplay', () => {{
            status.textContent = 'Ready to play';
            status.className = 'status';
        }});

        audio.addEventListener('playing', () => {{
            status.textContent = 'Now playing';
            status.className = 'status playing';
        }});

        audio.addEventListener('pause', () => {{
            status.textContent = 'Paused';
            status.className = 'status';
        }});

        audio.addEventListener('ended', () => {{
            status.textContent = 'Song ended';
            status.className = 'status';
        }});

        audio.addEventListener('error', (e) => {{
            console.error('Audio error:', e);
            status.textContent = 'Error loading audio. Please check the file link.';
            status.className = 'status error';
        }});

        // Handle album art loading error
        albumArt.addEventListener('error', () => {{
            albumArt.style.display = 'none';
            console.error('Error loading album art');
        }});

        // Attempt to autoplay (may be blocked by browser policies)
        // User interaction may be required for autoplay to work
        window.addEventListener('load', () => {{
            // Try to play, but handle if autoplay is blocked
            const playPromise = audio.play();

            if (playPromise !== undefined) {{
                playPromise
                    .then(() => {{
                        // Autoplay started successfully
                        console.log('Autoplay started');
                    }})
                    .catch(error => {{
                        // Autoplay was prevented
                        console.log('Autoplay prevented:', error);
                        status.textContent = 'Click play to start';
                        status.className = 'status';
                    }});
            }}
        }});
    </script>
</body>
</html>"""

    return html_content

# New helper: central player (single page that reads ?id=...)
def generate_central_player(output_dir):
    """
    Generate docs/player.html — single central player that reads ?id=song_id
    and loads docs/onedrive_files.json to populate UI. Scrapers won't execute JS, so per-song
    stub pages provide OG tags for previews.
    Features: Custom controls without download button, Share button, time slider in separate row.
    """
    player_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Player - Karnlada Songs</title>
<meta name="description" content="Music player">
<style>
/* minimal styles reused from previous players */
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.player-container{background:rgba(255,255,255,.95);border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.3);max-width:400px;width:100%;overflow:hidden;backdrop-filter:blur(10px)}
.album-art-wrapper{position:relative;width:100%;aspect-ratio:1;overflow:hidden;cursor:pointer}
.album-art{width:100%;height:100%;object-fit:cover;display:block}
.play-pause-btn{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;border-radius:50%;background:rgba(255,255,255,0.95);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);transition:all 0.2s;z-index:10}
.play-pause-btn:hover{transform:translate(-50%,-50%) scale(1.1);background:rgba(255,255,255,1)}
.play-pause-btn.playing{opacity:0;pointer-events:none}
.play-pause-btn svg{width:35px;height:35px;fill:#667eea}
.player-info{padding:30px;text-align:center}
.song-title{font-size:24px;font-weight:700;color:#2d3748;margin-bottom:8px;line-height:1.3}
.artist-name{font-size:18px;color:#718096;margin-bottom:20px}
.controls-section{margin-top:20px}
.time-slider-row{margin-bottom:15px}
.time-slider{-webkit-appearance:none;appearance:none;width:100%;height:6px;border-radius:3px;background:#e2e8f0;outline:none;cursor:pointer}
.time-slider::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:18px;height:18px;border-radius:50%;background:#667eea;cursor:pointer}
.time-slider::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:#667eea;cursor:pointer;border:none}
.time-display{display:flex;justify-content:space-between;font-size:12px;color:#718096;margin-top:5px}
.button-row{display:flex;gap:10px;align-items:center;justify-content:center}
.ctrl-btn{background:#667eea;color:white;border:none;border-radius:8px;padding:10px 20px;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.2s;flex:1;max-width:120px}
.ctrl-btn:hover{background:#5568d3;transform:translateY(-1px)}
.ctrl-btn:active{transform:translateY(0)}
.share-btn{background:#48bb78}
.share-btn:hover{background:#38a169}
.status{margin-top:15px;font-size:14px;color:#a0aec0;font-style:italic}
.status.loading{color:#667eea}.status.playing{color:#48bb78}.status.error{color:#f56565}
audio{display:none}
@media (max-width:480px){
.song-title{font-size:20px}
.artist-name{font-size:16px}
.player-info{padding:20px}
.play-pause-btn{width:70px;height:70px}
.play-pause-btn svg{width:30px;height:30px}
}
</style>
</head>
<body>
<div class="player-container" id="player">
	<div class="album-art-wrapper" id="albumWrapper">
		<img src="" alt="album art" class="album-art" id="albumArt">
		<button class="play-pause-btn" id="playPauseBtn">
			<svg viewBox="0 0 24 24" id="playIcon">
				<path d="M8 5v14l11-7z"/>
			</svg>
			<svg viewBox="0 0 24 24" id="pauseIcon" style="display:none">
				<path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
			</svg>
		</button>
	</div>
	<div class="player-info">
		<h1 class="song-title" id="songTitle">Loading...</h1>
		<p class="artist-name" id="artistName"></p>

		<div class="controls-section">
			<div class="time-slider-row">
				<input type="range" class="time-slider" id="timeSlider" min="0" max="100" value="0">
				<div class="time-display">
					<span id="currentTime">0:00</span>
					<span id="duration">0:00</span>
				</div>
			</div>
			<div class="button-row">
				<button class="ctrl-btn" id="playBtn">▶ Play</button>
				<button class="ctrl-btn share-btn" id="shareBtn">📤 Share</button>
			</div>
		</div>

		<audio id="audioPlayer">
			Your browser does not support the audio element.
		</audio>
		<div class="status" id="status">Loading...</div>
	</div>
</div>

<script>
let currentFile = null;

async function fetchJSON(path){
	try{
		const r = await fetch(path);
		if(!r.ok) throw new Error('Fetch failed');
		return await r.json();
	}catch(e){
		console.error(e);
		return null;
	}
}

function getQueryParam(name){
	const params = new URLSearchParams(location.search);
	return params.get(name);
}

function setStatus(text, cls=''){
	const s = document.getElementById('status');
	s.textContent = text;
	s.className = 'status' + (cls? ' ' + cls : '');
}

function selectFile(files, id){
	if(!id) return files[0];
	// First try matching by song_id (stable ID)
	for(const f of files){
		if(f.song_id === id) return f;
	}
	// if id is numeric index
	if(/^\d+$/.test(id)){
		const idx = parseInt(id,10)-1;
		return files[idx] || files[0];
	}
	// try matching by filename or title (backward compatibility)
	for(const f of files){
		if(f.html_filename === id || f.html_filename.replace('.html','') === id) return f;
		if(f.title === id) return f;
	}
	return files[0];
}

function formatTime(seconds){
	if(isNaN(seconds)) return '0:00';
	const mins = Math.floor(seconds / 60);
	const secs = Math.floor(seconds % 60);
	return `${mins}:${secs.toString().padStart(2,'0')}`;
}

function togglePlayPause(){
	const audioEl = document.getElementById('audioPlayer');
	if(audioEl.paused){
		audioEl.play();
	}else{
		audioEl.pause();
	}
}

function updatePlayPauseButton(){
	const audioEl = document.getElementById('audioPlayer');
	const playPauseBtn = document.getElementById('playPauseBtn');
	const playBtn = document.getElementById('playBtn');

	if(audioEl.paused){
		playPauseBtn.classList.remove('playing');
		playBtn.textContent = '▶ Play';
	}else{
		playPauseBtn.classList.add('playing');
		playBtn.textContent = '⏸ Pause';
	}
}

async function shareCurrentSong(){
	if(!currentFile) return;

	const shareData = {
		title: currentFile.title,
		text: `Listen to "${currentFile.title}" by ${currentFile.artist}`,
		url: window.location.href
	};

	// Check if Web Share API is supported
	if(navigator.share){
		try{
			await navigator.share(shareData);
			setStatus('Shared successfully!', 'playing');
		}catch(err){
			if(err.name !== 'AbortError'){
				console.error('Share failed:', err);
				fallbackShare();
			}
		}
	}else{
		fallbackShare();
	}
}

function fallbackShare(){
	// Fallback: copy URL to clipboard
	const url = window.location.href;
	if(navigator.clipboard){
		navigator.clipboard.writeText(url).then(()=>{
			setStatus('Link copied to clipboard!', 'playing');
		}).catch(()=>{
			setStatus('Could not copy link', 'error');
		});
	}else{
		setStatus('Sharing not supported', 'error');
	}
}

(async function(){
	const filesData = await fetchJSON('onedrive_files.json');
	if(!filesData || !filesData.files || filesData.files.length===0){
		setStatus('No files found', 'error');
		return;
	}
	const files = filesData.files;
	const id = getQueryParam('id');
	const file = selectFile(files, id);
	currentFile = file;

	// populate UI
	document.getElementById('songTitle').textContent = file.title;
	document.getElementById('artistName').textContent = file.artist;
	const art = document.getElementById('albumArt');
	art.src = file.album_art_url || 'images/album_art_karnlada.jpg';
	art.alt = file.title + ' album art';

	const audioEl = document.getElementById('audioPlayer');
	// clear existing sources
	while(audioEl.firstChild) audioEl.removeChild(audioEl.firstChild);
	const src = document.createElement('source');
	src.src = file.audio_url;
	src.type = 'audio/mpeg';
	audioEl.appendChild(src);
	// optional mp4 source
	const src2 = document.createElement('source');
	src2.src = file.audio_url;
	src2.type = 'audio/mp4';
	audioEl.appendChild(src2);

	// Control bindings
	const playPauseBtn = document.getElementById('playPauseBtn');
	const playBtn = document.getElementById('playBtn');
	const shareBtn = document.getElementById('shareBtn');
	const albumWrapper = document.getElementById('albumWrapper');
	const timeSlider = document.getElementById('timeSlider');
	const currentTimeEl = document.getElementById('currentTime');
	const durationEl = document.getElementById('duration');

	playPauseBtn.addEventListener('click', (e)=>{
		e.stopPropagation();
		togglePlayPause();
	});

	playBtn.addEventListener('click', togglePlayPause);
	albumWrapper.addEventListener('click', togglePlayPause);
	shareBtn.addEventListener('click', shareCurrentSong);

	// Time slider
	let isSeeking = false;
	timeSlider.addEventListener('input', ()=>{
		isSeeking = true;
		const time = (timeSlider.value / 100) * audioEl.duration;
		currentTimeEl.textContent = formatTime(time);
	});

	timeSlider.addEventListener('change', ()=>{
		const time = (timeSlider.value / 100) * audioEl.duration;
		audioEl.currentTime = time;
		isSeeking = false;
	});

	// Audio events
	audioEl.addEventListener('loadstart', ()=> setStatus('Loading audio...', 'loading'));
	audioEl.addEventListener('canplay', ()=> setStatus('Ready to play'));
	audioEl.addEventListener('playing', ()=>{
		setStatus('Now playing', 'playing');
		updatePlayPauseButton();
	});
	audioEl.addEventListener('pause', ()=>{
		setStatus('Paused');
		updatePlayPauseButton();
	});
	audioEl.addEventListener('ended', ()=>{
		setStatus('Song ended');
		updatePlayPauseButton();
	});
	audioEl.addEventListener('error', ()=> setStatus('Error loading audio', 'error'));

	audioEl.addEventListener('loadedmetadata', ()=>{
		durationEl.textContent = formatTime(audioEl.duration);
	});

	audioEl.addEventListener('timeupdate', ()=>{
		if(!isSeeking){
			const percent = (audioEl.currentTime / audioEl.duration) * 100;
			timeSlider.value = percent || 0;
			currentTimeEl.textContent = formatTime(audioEl.currentTime);
		}
	});

	// try to autoplay if allowed
	try{ await audioEl.play(); }catch(e){ setStatus('Click play to start'); }
})();
</script>
</body>
</html>
"""
    with open(os.path.join(output_dir, 'player.html'), 'w', encoding='utf-8') as f:
        f.write(player_html)
    print("✓ Generated: player.html")

# New helper: per-song stub with OG tags + immediate redirect to player.html?id=...
def generate_stub_page(file_info, base_url, output_dir):
    """
    Generate a stub page with Open Graph tags and a redirect to the central player.
    """
    title = escape(file_info['title'])
    artist = escape(file_info['artist'])
    audio_url = escape(file_info['audio_url'])
    album_art_url = escape(file_info['album_art_url'])
    html_filename = file_info['html_filename']

    # Generate a unique ID for the song based on its title and artist
    unique_id = hashlib.md5(f"{title}-{artist}".encode('utf-8')).hexdigest()[:8]

    page_url = f"{base_url}/{html_filename}"
    player_target = f"player.html?id={unique_id}"

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} - {artist}</title>

<!-- Open Graph tags for scrapers (WhatsApp, Messenger) -->
<meta property="og:type" content="music.song">
<meta property="og:title" content="{title}">
<meta property="og:description" content="Artist: {artist}">
<meta property="og:image" content="{album_art_url}">
<meta property="og:audio" content="{audio_url}">
<meta property="music:musician" content="{artist}">
<meta property="og:url" content="{page_url}">

<!-- Twitter -->
<meta name="twitter:card" content="player">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="Artist: {artist}">
<meta name="twitter:image" content="{album_art_url}">

<!-- Redirect immediately to central player (client-side) -->
<meta http-equiv="refresh" content="0; url={player_target}">
<link rel="canonical" href="{player_target}">
</head>
<body>
<p>If you are not redirected, <a href="{player_target}">open player</a>.</p>
</body>
</html>"""

    with open(os.path.join(output_dir, html_filename), 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✓ Generated stub: {html_filename}")

def main():
    # Load the song data from onedrive_files.json
    input_file = 'onedrive_files.json'

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        print("Please run list_onedrive_files.py first.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    files = data.get('files', [])

    if not files:
        print("No files found in the JSON. Please add files to list_onedrive_files.py")
        return

    # GitHub Pages base URL
    base_url = "https://kacharuk.github.io/karnlada_songs"

    # Create output directory for HTML files
    output_dir = 'docs'  # GitHub Pages can serve from /docs folder
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating stub pages for {len(files)} song(s)...\n")

    for file_info in files:
        # Ensure html_filename exists
        if not file_info.get('html_filename'):
            safe_title = "".join(c for c in file_info['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_').lower()
            file_info['html_filename'] = f"{safe_title}.html"

        # Generate a stub page for each song
        generate_stub_page(file_info, base_url, output_dir)

    print(f"\nAll stub pages generated in '{output_dir}/' directory")

if __name__ == "__main__":
    main()
