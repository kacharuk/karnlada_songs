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
    Generate docs/player.html — single central player that reads ?id=filename (or numeric index)
    and loads docs/onedrive_files.json to populate UI. Scrapers won't execute JS, so per-song
    stub pages provide OG tags for previews.
    """
    player_html = """<!DOCTYPE html>
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
.album-art{width:100%;aspect-ratio:1;object-fit:cover;display:block}
.player-info{padding:30px;text-align:center}
.song-title{font-size:24px;font-weight:700;color:#2d3748;margin-bottom:8px;line-height:1.3}
.artist-name{font-size:18px;color:#718096;margin-bottom:25px}
.audio-controls{width:100%;margin-top:20px;outline:none}
audio{width:100%;height:40px;border-radius:20px}
.status{margin-top:15px;font-size:14px;color:#a0aec0;font-style:italic}
.status.loading{color:#667eea}.status.playing{color:#48bb78}.status.error{color:#f56565}
</style>
</head>
<body>
<div class="player-container" id="player">
	<img src="" alt="album art" class="album-art" id="albumArt">
	<div class="player-info">
		<h1 class="song-title" id="songTitle">Loading...</h1>
		<p class="artist-name" id="artistName"></p>
		<audio id="audioPlayer" class="audio-controls" controls>
			Your browser does not support the audio element.
		</audio>
		<div class="status" id="status">Loading...</div>
	</div>
</div>

<script>
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
	// if id is numeric index
	if(/^\d+$/.test(id)){
		const idx = parseInt(id,10)-1;
		return files[idx] || files[0];
	}
	// try matching by filename or title
	for(const f of files){
		if(f.html_filename === id || f.html_filename.replace('.html','') === id) return f;
		if(f.title === id) return f;
	}
	return files[0];
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

	// events
	audioEl.addEventListener('loadstart', ()=> setStatus('Loading audio...', 'loading'));
	audioEl.addEventListener('canplay', ()=> setStatus('Ready to play'));
	audioEl.addEventListener('playing', ()=> setStatus('Now playing', 'playing'));
	audioEl.addEventListener('pause', ()=> setStatus('Paused'));
	audioEl.addEventListener('ended', ()=> setStatus('Song ended'));
	audioEl.addEventListener('error', ()=> setStatus('Error loading audio', 'error'));

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
    Write a minimal HTML file containing OG meta tags (title, image, audio)
    and a meta-refresh / link to docs/player.html?id={html_filename}.
    This static page ensures WhatsApp/other scrapers get proper preview.
    """
    page_filename = file_info['html_filename']
    page_url = f"{base_url}/{page_filename}"
    player_target = f"player.html?id={page_filename}"
    og_image = file_info.get('album_art_url','images/album_art_karnlada.jpg')
    og_audio = file_info.get('audio_url','')
    title = escape(file_info['title'])
    artist = escape(file_info['artist'])

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} - {artist}</title>

<!-- Open Graph tags for scrapers (WhatsApp, Messenger) -->
<meta property="og:type" content="music.song">
<meta property="og:title" content="{title}">
<meta property="og:description" content="Artist: {artist}">
<meta property="og:image" content="{og_image}">
<meta property="og:audio" content="{og_audio}">
<meta property="music:musician" content="{artist}">
<meta property="og:url" content="{page_url}">

<!-- Twitter -->
<meta name="twitter:card" content="player">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="Artist: {artist}">
<meta name="twitter:image" content="{og_image}">

<!-- Redirect immediately to central player (client-side) -->
<meta http-equiv="refresh" content="0; url={player_target}">
<link rel="canonical" href="{player_target}">
</head>
<body>
<p>If you are not redirected, <a href="{player_target}">open player</a>.</p>
</body>
</html>"""
    with open(os.path.join(output_dir, page_filename), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ Generated stub: {page_filename}")

def main():
    # Load the OneDrive files JSON
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

    generated_files = []

    print(f"Generating stub pages + central player for {len(files)} song(s)...\n")

    # Create/refresh docs/onedrive_files.json so the central player can fetch it
    with open(os.path.join(output_dir, 'onedrive_files.json'), 'w', encoding='utf-8') as f:
        json.dump({'files': files}, f, indent=2, ensure_ascii=False)
    print("✓ Copied: docs/onedrive_files.json")

    for idx, file_info in enumerate(files, 1):
        # ensure html_filename exists
        html_filename = file_info.get('html_filename') or f"song_{idx}.html"
        file_info['html_filename'] = html_filename

        # generate a lightweight stub with OG tags + redirect to central player
        generate_stub_page(file_info, base_url, output_dir)

        page_url = f"{base_url}/{html_filename}"
        generated_files.append({
            'title': file_info['title'],
            'artist': file_info['artist'],
            'filename': html_filename,
            'url': page_url
        })

        print(f"  stub created: {html_filename}")

    # Copy generated_urls.json into docs/
    with open(os.path.join(output_dir, 'generated_urls.json'), 'w', encoding='utf-8') as f:
        json.dump(generated_files, f, indent=2, ensure_ascii=False)
    print("✓ Copied: docs/generated_urls.json")

    # generate central player
    generate_central_player(output_dir)

    # regenerate index to point to stubs
    generate_index_page(generated_files, output_dir, base_url)

    print(f"\nAll files generated in '{output_dir}/' directory")
    print(f"URL list saved to: docs/generated_urls.json")
    print(f"\nNext step: Push to GitHub to deploy on GitHub Pages")

def generate_index_page(files_list, output_dir, base_url):
    """Generate an index page organized by albums"""

    # Load full file data from onedrive_files.json to get album info
    with open('onedrive_files.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    full_files = data.get('files', [])

    # Group files by album
    albums = {}
    for file_info in full_files:
        album = file_info.get('album', 'Unknown Album')
        if album not in albums:
            albums[album] = []
        albums[album].append(file_info)

    # Sort albums alphabetically
    sorted_albums = sorted(albums.items())

    # Build HTML for each album section
    albums_html = ""
    for album_name, songs in sorted_albums:
        # Sort songs alphabetically by title
        songs_sorted = sorted(songs, key=lambda x: x['title'])

        songs_html = ""
        for song in songs_sorted:
            songs_html += f"""
                    <div class="song-item">
                        <span class="song-title">{escape(song['title'])}</span>
                        <div class="song-actions">
                            <a href="{song['html_filename']}" class="play-button">▶ Play</a>
                        </div>
                    </div>"""

        albums_html += f"""
        <div class="album-section">
            <h2 class="album-title">📀 {escape(album_name)}</h2>
            <div class="songs-list">
                {songs_html}
            </div>
        </div>"""

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Karnlada Songs - Music Collection</title>
    <meta property="og:title" content="Karnlada Songs">
    <meta property="og:description" content="Complete music collection organized by albums">
    <meta property="og:type" content="website">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 40px;
            font-size: 42px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .album-section {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .album-title {{
            color: #2d3748;
            font-size: 28px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}

        .songs-list {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .song-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: #f7fafc;
            border-radius: 10px;
            transition: all 0.2s;
        }}

        .song-item:hover {{
            background: #edf2f7;
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .song-title {{
            color: #2d3748;
            font-size: 18px;
            font-weight: 500;
        }}

        .song-actions {{
            display: flex;
            gap: 10px;
        }}

        .play-button {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            text-decoration: none;
            font-weight: 600;
            background: #667eea;
            color: white;
            transition: all 0.2s;
            font-size: 14px;
        }}

        .play-button:hover {{
            background: #5568d3;
            transform: scale(1.05);
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 32px;
            }}

            .album-title {{
                font-size: 24px;
            }}

            .song-item {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}

            .song-actions {{
                width: 100%;
            }}

            .play-button {{
                width: 100%;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Karnlada Songs</h1>
        {albums_html}
    </div>
</body>
</html>"""

    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Generated: index.html")
    print(f"  URL: {base_url}/index.html")

if __name__ == "__main__":
    main()
