#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to scan local audio files and generate metadata.
Scans docs/audio/ folder structure organized by albums.
"""

import json
import os
import sys
from urllib.parse import quote

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def extract_song_info(filename, album_folder):
    """
    Extract song title and artist from filename.
    Expected format: "Song Title - Artist Name.mp3"
    Removes numbering prefix like "01", "02กล้วยไม้" etc.
    """
    # Remove extension
    name = os.path.splitext(filename)[0]

    # Remove numbering prefix (e.g., "01", "02. ", "03 กล้วยไม้" at the start
    import re
    # Match patterns like "01", "02.", "03. ", "04 " at the beginning
    name = re.sub(r'^\d+\.?\s*', '', name)

    # Try to split by ' - '
    if ' - ' in name:
        parts = name.split(' - ', 1)
        title = parts[0].strip()
        artist = parts[1].strip() if len(parts) > 1 else "กาญจน์ลดา มฤคพิทักษ์"
    else:
        title = name
        artist = "กาญจน์ลดา มฤคพิทักษ์"

    return title, artist

def scan_audio_folders(audio_base_path='docs/audio'):
    """
    Scan all album folders in docs/audio/ and collect song information.
    Returns a list of song dictionaries.
    """
    files = []

    if not os.path.exists(audio_base_path):
        print(f"Warning: {audio_base_path} does not exist!")
        return files

    # Scan each album folder
    album_folders = []
    for item in os.listdir(audio_base_path):
        item_path = os.path.join(audio_base_path, item)
        if os.path.isdir(item_path):
            album_folders.append(item)

    album_folders.sort()  # Sort alphabetically

    print(f"Found {len(album_folders)} album folder(s):\n")

    for album_folder in album_folders:
        album_path = os.path.join(audio_base_path, album_folder)

        # Find all audio files in this album
        audio_files = []
        for filename in os.listdir(album_path):
            if filename.lower().endswith(('.mp3', '.m4a')):
                audio_files.append(filename)

        audio_files.sort()  # Sort songs alphabetically

        print(f"📁 {album_folder}: {len(audio_files)} songs")

        # Check for album art in this folder
        album_art_path = os.path.join(album_path, 'album_art.jpg')
        if os.path.exists(album_art_path):
            album_art_url = f"audio/{album_folder}/album_art.jpg"
        else:
            # Fall back to default album art
            album_art_url = "images/album_art_karnlada.jpg"

        for filename in audio_files:
            title, artist = extract_song_info(filename, album_folder)

            # Build relative path from docs/ folder
            # e.g., "audio/Karnlada Music/song.mp3"
            audio_url = f"audio/{album_folder}/{filename}"

            files.append({
                "title": title,
                "artist": artist,
                "album": album_folder,
                "audio_url": audio_url,
                "album_art_url": album_art_url
            })

    print(f"\nTotal songs scanned: {len(files)}\n")
    return files

def generate_html_filename(title):
    """
    Generate a safe HTML filename from song title.
    Keeps Thai characters but removes special chars.
    """
    # Remove characters that could cause issues in URLs
    safe_chars = []
    for char in title:
        if char.isalnum() or char in (' ', '-', '_'):
            safe_chars.append(char)

    safe_title = ''.join(safe_chars).strip()

    # Replace spaces with nothing (or could use '-')
    safe_title = safe_title.replace(' ', '')

    return f"{safe_title}.html"

def main():
    print("Scanning local audio files from docs/audio/...\n")

    files = scan_audio_folders('docs/audio')

    if not files:
        print("\n" + "="*60)
        print("No audio files found!")
        print("="*60)
        print("\nPlease ensure audio files are in docs/audio/ organized by album folders.")
        output = {
            "files": [],
            "count": 0
        }
    else:
        # Add html_filename to each file
        for file_info in files:
            file_info['html_filename'] = generate_html_filename(file_info['title'])

        output = {
            "files": files,
            "count": len(files)
        }

        print("="*60)
        print(f"Successfully scanned {len(files)} song(s) from {len(set(f['album'] for f in files))} album(s)")
        print("="*60)

        # Show summary by album
        albums = {}
        for file in files:
            album = file['album']
            if album not in albums:
                albums[album] = []
            albums[album].append(file['title'])

        print("\nAlbum summary:")
        for album, songs in sorted(albums.items()):
            print(f"  {album}: {len(songs)} songs")

    # Save to JSON file
    output_file = 'onedrive_files.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nOutput saved to: {output_file}")
    return output

if __name__ == "__main__":
    main()
