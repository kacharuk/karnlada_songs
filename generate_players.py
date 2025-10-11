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

    print(f"Generating HTML players for {len(files)} song(s)...\n")

    for file_info in files:
        html_content = generate_html_player(file_info, base_url)
        html_filename = file_info['html_filename']
        output_path = os.path.join(output_dir, html_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        page_url = f"{base_url}/{html_filename}"
        generated_files.append({
            'title': file_info['title'],
            'artist': file_info['artist'],
            'filename': html_filename,
            'url': page_url
        })

        print(f"✓ Generated: {html_filename}")
        print(f"  URL: {page_url}\n")

    # Generate index.html with links to all songs
    generate_index_page(generated_files, output_dir, base_url)

    # Save URL list
    with open('generated_urls.json', 'w', encoding='utf-8') as f:
        json.dump(generated_files, f, indent=2, ensure_ascii=False)

    print(f"\nAll files generated in '{output_dir}/' directory")
    print(f"URL list saved to: generated_urls.json")
    print(f"\nNext step: Push to GitHub to deploy on GitHub Pages")

def generate_index_page(files, output_dir, base_url):
    """Generate an index page with links to all songs"""

    songs_list = ""
    for file in files:
        songs_list += f"""
        <div class="song-item">
            <h3>{escape(file['title'])}</h3>
            <p class="artist">{escape(file['artist'])}</p>
            <a href="{file['filename']}" class="play-button">Play</a>
            <a href="{file['url']}" class="share-button">Share Link</a>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Karnlada Songs</title>
    <meta property="og:title" content="Karnlada Songs">
    <meta property="og:description" content="Music collection">
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
            max-width: 800px;
            margin: 0 auto;
        }}

        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 40px;
            font-size: 36px;
        }}

        .song-item {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .song-item h3 {{
            color: #2d3748;
            margin-bottom: 5px;
        }}

        .artist {{
            color: #718096;
            margin-bottom: 15px;
        }}

        .play-button, .share-button {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            margin-right: 10px;
            margin-top: 5px;
        }}

        .play-button {{
            background: #667eea;
            color: white;
        }}

        .share-button {{
            background: #48bb78;
            color: white;
        }}

        .play-button:hover {{
            background: #5568d3;
        }}

        .share-button:hover {{
            background: #38a169;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Karnlada Songs</h1>
        {songs_list}
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
