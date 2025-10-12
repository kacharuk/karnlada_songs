#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete HTML generation script for Karnlada Songs
Generates:
- Enhanced player.html with playlist support
- Enhanced index.html with search, share, QR codes, and playlist buttons
- Individual song stub pages
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

def generate_enhanced_player(output_dir):
    """Generate player.html with playlist support and modular JavaScript"""

    player_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Player - Karnlada Songs</title>
<meta name="description" content="Music player">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-N35GFR9ZDS"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-N35GFR9ZDS');
</script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:20px}
.player-container{background:rgba(255,255,255,.95);border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.3);max-width:400px;width:100%;overflow:hidden;backdrop-filter:blur(10px);margin-bottom:20px}
.album-art-wrapper{position:relative;width:100%;aspect-ratio:1;overflow:hidden;cursor:pointer}
.album-art{width:100%;height:100%;object-fit:cover;display:block}
.play-pause-btn{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;border-radius:50%;background:rgba(255,255,255,0.95);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);transition:all 0.2s;z-index:10}
.play-pause-btn:hover{transform:translate(-50%,-50%) scale(1.1);background:rgba(255,255,255,1)}
.play-pause-btn.playing{opacity:0;pointer-events:none}
.play-pause-btn svg{width:35px;height:35px;fill:#667eea}
.player-info{padding:30px;text-align:center}
.song-title{font-size:24px;font-weight:700;color:#2d3748;margin-bottom:8px;line-height:1.3}
.artist-name{font-size:18px;color:#718096;margin-bottom:10px}
.next-song{font-size:14px;color:#718096;margin-top:10px}
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
#playlistContainer{background:rgba(255,255,255,.95);border-radius:16px;padding:20px;max-width:600px;width:100%;display:none;max-height:300px;overflow-y:auto}
#playlistContainer h3{color:#2d3748;margin-bottom:15px;font-size:18px}
.playlist-song-item{padding:12px;margin-bottom:8px;background:#f7fafc;border-radius:8px;display:flex;align-items:center;gap:12px;transition:all 0.2s}
.playlist-song-item:hover{background:#edf2f7}
.playlist-song-item.playing{background:#e6fffa;border-left:4px solid #48bb78}
.playlist-song-item.external{opacity:0.6;cursor:not-allowed}
.playlist-indicator{min-width:25px;font-weight:700;color:#667eea;text-align:center}
.playlist-song-item.playing .playlist-indicator{color:#48bb78}
.playlist-song-title{color:#2d3748;font-size:14px}
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
<div class="player-container">
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
		<p class="next-song" id="nextSong" style="display:none"></p>
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
		<audio id="audioPlayer">Your browser does not support the audio element.</audio>
		<div class="status" id="status">Loading...</div>
	</div>
</div>
<div id="playlistContainer">
	<h3>Playlist</h3>
	<div id="playlistSongs"></div>
</div>
<script src="js/utils.js"></script>
<script src="js/player.js"></script>
</body>
</html>
"""

    with open(os.path.join(output_dir, 'player.html'), 'w', encoding='utf-8') as f:
        f.write(player_html)
    print("✓ Generated: player.html")

def generate_stub_page(file_info, base_url, output_dir):
    """Generate individual song stub pages with OG tags"""
    page_filename = file_info['html_filename']
    page_url = f"{base_url}/songs/{page_filename}"
    song_id = file_info.get('song_id', page_filename.replace('.html', ''))
    is_external = file_info.get('is_external', False)

    if is_external:
        player_target = file_info.get('audio_url', '')
    else:
        player_target = f"../player.html?id={song_id}"

    og_image = file_info.get('album_art_url','images/album_art_karnlada.jpg')
    og_audio = file_info.get('audio_url','')
    title = escape(file_info['title'])
    artist = escape(file_info['artist'])

    if is_external:
        og_audio_tag = f'<meta property="og:audio" content="{og_audio}">'
        og_image_tag = f'<meta property="og:image" content="{base_url}/{og_image}">'
        redirect_text = "Redirecting to external link..."
        link_text = "click here to open"
    else:
        og_audio_tag = f'<meta property="og:audio" content="../{og_audio}">'
        og_image_tag = f'<meta property="og:image" content="../{og_image}">'
        redirect_text = "If you are not redirected,"
        link_text = "open player"

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} - {artist}</title>
<meta property="og:type" content="music.song">
<meta property="og:title" content="{title}">
<meta property="og:description" content="Artist: {artist}">
{og_image_tag}
{og_audio_tag}
<meta property="music:musician" content="{artist}">
<meta property="og:url" content="{page_url}">
<meta name="twitter:card" content="player">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="Artist: {artist}">
<meta name="twitter:image" content="../{og_image}">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-N35GFR9ZDS"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-N35GFR9ZDS');
</script>
<meta http-equiv="refresh" content="0; url={player_target}">
<link rel="canonical" href="{player_target}">
</head>
<body>
<p>{redirect_text} <a href="{player_target}">{link_text}</a>.</p>
</body>
</html>"""

    songs_dir = os.path.join(output_dir, 'songs')
    os.makedirs(songs_dir, exist_ok=True)

    with open(os.path.join(songs_dir, page_filename), 'w', encoding='utf-8') as f:
        f.write(html)

def load_songs_from_csv(csv_path='songs_mapping.csv'):
    """Load songs from CSV file"""
    import csv
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'song_id': row['song_id'],
                'album': row['album'],
                'title': row['title'],
                'artist': row['artist'],
                'audio_url': row['audio_file_path'],
                'html_filename': row['html_filename'],
                'is_external': row.get('is_external', 'false').lower() == 'true',
                'album_art_url': ''  # Will be populated from file system
            })
    return songs

def generate_enhanced_index(files_list, output_dir, base_url):
    """Generate enhanced index.html with search, share, QR codes, and playlist support"""

    # Load full file data from CSV
    full_files = load_songs_from_csv('songs_mapping.csv')

    # Group by album
    albums = {}
    for file_info in full_files:
        album = file_info.get('album', 'Unknown Album')
        if album not in albums:
            albums[album] = []
        albums[album].append(file_info)

    sorted_albums = sorted(albums.items())

    # Build album index
    album_index = ""
    for album_name, songs in sorted_albums:
        album_id = album_name.replace(' ', '-').replace('/', '-')
        album_index += f'\n            <a href="#{album_id}" class="album-link">📀 {escape(album_name)} ({len(songs)})</a>'

    # Build HTML for each album
    albums_html = ""
    for album_name, songs in sorted_albums:
        album_id = album_name.replace(' ', '-').replace('/', '-')
        # Keep songs in CSV order (no sorting)

        # Collect song IDs for playlist
        song_ids = [s.get('song_id', s['html_filename'].replace('.html', '')) for s in songs]
        playlist_ids = ','.join(song_ids)

        songs_html = ""
        for song in songs:
            song_id = song.get('song_id', song['html_filename'].replace('.html', ''))
            share_url = f"{base_url}/songs/{song['html_filename']}"

            songs_html += f"""
                    <div class="song-item" data-song-id="{song_id}">
                        <span class="song-title">{escape(song['title'])}</span>
                        <div class="song-actions">
                            <a href="songs/{song['html_filename']}" class="action-btn play-button">▶ Play</a>
                            <button class="action-btn share-button" onclick="handleShare('{escape(share_url, quote=True)}', '{escape(song['title'], quote=True)}', '{escape(song['artist'], quote=True)}')">📤 Share</button>
                            <button class="action-btn qr-button" onclick="handleQR('{escape(share_url, quote=True)}', '{escape(song['title'], quote=True)}')">🔳 QR</button>
                        </div>
                    </div>"""

        albums_html += f"""
        <div class="album-section" id="{album_id}">
            <div class="album-header">
                <h2 class="album-title">📀 {escape(album_name)}</h2>
                <a href="player.html?ids={playlist_ids}" class="playlist-button">▶ Play Playlist ({len(songs)})</a>
            </div>
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
    <meta property="og:description" content="Karnlada's Music Collection">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://kacharuk.github.io/karnlada_songs/images/album_art_karnlada.jpg">
    <meta property="og:image:secure_url" content="https://kacharuk.github.io/karnlada_songs/images/album_art_karnlada.jpg">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="1200">
    <meta property="og:image:alt" content="Karnlada Songs Album Art">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-N35GFR9ZDS"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-N35GFR9ZDS');
    </script>
    <style>
        * {{margin:0;padding:0;box-sizing:border-box}}
        body {{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:40px 20px}}
        .container {{max-width:900px;margin:0 auto}}
        h1 {{color:white;text-align:center;margin-bottom:30px;font-size:42px;text-shadow:2px 2px 4px rgba(0,0,0,0.2)}}

        .search-container {{background:rgba(255,255,255,0.95);border-radius:16px;padding:20px;margin-bottom:30px;box-shadow:0 10px 30px rgba(0,0,0,0.15)}}
        .search-box {{position:relative;display:flex;gap:10px}}
        #searchInput {{flex:1;padding:15px 20px;font-size:16px;border:2px solid #e2e8f0;border-radius:12px;outline:none;transition:border-color 0.2s}}
        #searchInput:focus {{border-color:#667eea}}
        #clearSearch {{display:none;padding:15px 25px;background:#f56565;color:white;border:none;border-radius:12px;cursor:pointer;font-weight:600;transition:background 0.2s}}
        #clearSearch:hover {{background:#e53e3e}}

        .album-index {{background:rgba(255,255,255,0.95);border-radius:16px;padding:25px;margin-bottom:30px;box-shadow:0 10px 30px rgba(0,0,0,0.15)}}
        .album-index h2 {{color:#2d3748;font-size:24px;margin-bottom:20px;text-align:center}}
        .album-links {{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}}
        .album-link {{display:inline-block;padding:10px 18px;background:#667eea;color:white;text-decoration:none;border-radius:20px;font-size:15px;font-weight:500;transition:all 0.2s}}
        .album-link:hover {{background:#5568d3;transform:translateY(-2px);box-shadow:0 4px 12px rgba(102,126,234,0.4)}}

        .album-section {{background:rgba(255,255,255,0.98);border-radius:16px;padding:30px;margin-bottom:30px;box-shadow:0 10px 30px rgba(0,0,0,0.2);scroll-margin-top:20px}}
        .album-header {{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:15px;border-bottom:3px solid #667eea;flex-wrap:wrap;gap:10px}}
        .album-title {{color:#2d3748;font-size:28px;margin:0}}
        .playlist-button {{padding:10px 20px;background:#48bb78;color:white;text-decoration:none;border-radius:20px;font-weight:600;font-size:14px;transition:all 0.2s;white-space:nowrap}}
        .playlist-button:hover {{background:#38a169;transform:translateY(-1px)}}

        .songs-list {{display:flex;flex-direction:column;gap:10px}}
        .song-item {{display:flex;justify-content:space-between;align-items:center;padding:15px 20px;background:#f7fafc;border-radius:10px;transition:all 0.2s}}
        .song-item:hover {{background:#edf2f7;transform:translateX(5px);box-shadow:0 2px 8px rgba(0,0,0,0.1)}}
        .song-title {{color:#2d3748;font-size:18px;font-weight:500;flex:1}}
        .song-actions {{display:flex;gap:10px;flex-wrap:wrap}}
        .action-btn {{padding:8px 16px;border-radius:20px;text-decoration:none;font-weight:600;background:#667eea;color:white;transition:all 0.2s;font-size:13px;border:none;cursor:pointer;white-space:nowrap}}
        .action-btn:hover {{transform:scale(1.05)}}
        .play-button {{background:#667eea}}
        .play-button:hover {{background:#5568d3}}
        .share-button {{background:#48bb78}}
        .share-button:hover {{background:#38a169}}
        .qr-button {{background:#ed8936}}
        .qr-button:hover {{background:#dd6b20}}

        @media (max-width:768px) {{
            h1 {{font-size:32px}}
            .album-title {{font-size:24px}}
            .song-item {{flex-direction:column;align-items:flex-start;gap:10px}}
            .song-actions {{width:100%}}
            .action-btn {{flex:1;text-align:center;min-width:70px}}
            .album-header {{flex-direction:column;align-items:flex-start}}
            .playlist-button {{width:100%;text-align:center}}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Karnlada Songs</h1>

        <div class="search-container">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="ค้นหาเพลง..." autocomplete="off">
                <button id="clearSearch">Clear</button>
            </div>
        </div>

        <div class="album-index">
            <h2>Albums</h2>
            <div class="album-links">
                {album_index}
            </div>
        </div>

        {albums_html}
    </div>

    <script src="js/utils.js"></script>
    <script src="js/search.js"></script>
    <script>
        async function handleShare(url, title, artist) {{
            const result = await shareSong(url, title, artist);
            if (result.success) {{
                if (result.method === 'clipboard') {{
                    alert('ลิงก์ถูกคัดลอกไปยังคลิปบอร์ดแล้ว!');
                }}
            }} else {{
                alert('ไม่สามารถแชร์ได้: ' + result.error);
            }}
        }}

        function handleQR(url, title) {{
            showQRCodeModal(url, title);
        }}
    </script>
</body>
</html>"""

    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Generated: index.html")
    print(f"  URL: {base_url}/index.html")

def main():
    csv_file = 'songs_mapping.csv'

    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        print("Please run scan_new_songs.py first to create the CSV file.")
        return

    # Load songs from CSV
    files = load_songs_from_csv(csv_file)

    if not files:
        print("No songs found in the CSV.")
        return

    base_url = "https://kacharuk.github.io/karnlada_songs"
    output_dir = 'docs'
    os.makedirs(output_dir, exist_ok=True)

    # Ensure js directory exists
    js_dir = os.path.join(output_dir, 'js')
    os.makedirs(js_dir, exist_ok=True)

    print(f"Generating HTML pages for {len(files)} song(s)...\n")

    # Generate stub pages
    for idx, file_info in enumerate(files, 1):
        if not file_info.get('html_filename'):
            file_info['html_filename'] = f"song_{idx}.html"
        generate_stub_page(file_info, base_url, output_dir)

    print()

    # Generate player
    generate_enhanced_player(output_dir)

    # Generate index
    generated_files = [{
        'title': f['title'],
        'artist': f['artist'],
        'filename': f['html_filename'],
        'url': f"{base_url}/songs/{f['html_filename']}"
    } for f in files]

    generate_enhanced_index(generated_files, output_dir, base_url)

    # Save songs data for player.js
    with open(os.path.join(output_dir, 'songs.json'), 'w', encoding='utf-8') as f:
        json.dump({'files': files}, f, indent=2, ensure_ascii=False)
    print("✓ Generated: docs/songs.json")

    print(f"\n✅ All HTML files generated in '{output_dir}/' directory")
    print(f"\nNext step: Push to GitHub to deploy on GitHub Pages")

if __name__ == "__main__":
    main()
