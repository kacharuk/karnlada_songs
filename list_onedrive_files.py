#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to scan local audio files and generate metadata.
Scans docs/audio/ folder structure organized by albums.
"""

import json
import os
import sys
import csv
import hashlib
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

def generate_stable_id(album, title, audio_file_path):
    """
    Generate a stable ID for a song based on album + title + path.
    Uses a hash to create a short, stable identifier.
    """
    # Create a unique string from album, title, and original path
    unique_string = f"{album}:{title}:{audio_file_path}"
    # Generate a short hash (first 8 characters of MD5)
    hash_object = hashlib.md5(unique_string.encode('utf-8'))
    return hash_object.hexdigest()[:8]

def load_existing_mappings(csv_path='songs_mapping.csv'):
    """
    Load existing song mappings from CSV.
    Returns a tuple: (id_mappings, external_songs)
    - id_mappings: dict mapping (album, title, audio_path) -> song_id
    - external_songs: list of song dicts for external links
    """
    id_mappings = {}
    external_songs = []

    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['album'], row['title'], row['audio_file_path'])
                id_mappings[key] = row['song_id']

                # If this is an external link, save it to preserve in output
                is_ext = row.get('is_external', 'false').strip().lower()
                if is_ext == 'true' or is_ext == '1' or is_ext == 'yes':
                    external_songs.append({
                        'song_id': row['song_id'],
                        'album': row['album'],
                        'title': row['title'],
                        'artist': row['artist'],
                        'audio_url': row['audio_file_path'],
                        'html_filename': row['html_filename'],
                        'is_external': True,
                        'album_art_url': 'images/album_art_karnlada.jpg'  # default for external
                    })

    return id_mappings, external_songs

def save_mappings_to_csv(files, csv_path='songs_mapping.csv'):
    """
    Save song mappings to CSV file.
    Each song gets a stable ID that won't change even if filename changes.
    """
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['song_id', 'album', 'title', 'artist', 'audio_file_path', 'html_filename', 'is_external']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for file_info in files:
            writer.writerow({
                'song_id': file_info['song_id'],
                'album': file_info['album'],
                'title': file_info['title'],
                'artist': file_info['artist'],
                'audio_file_path': file_info['audio_url'],
                'html_filename': file_info['html_filename'],
                'is_external': file_info.get('is_external', 'false')
            })

    print(f"✓ Saved mappings to: {csv_path}")

def main():
    print("Scanning local audio files from docs/audio/...\n")

    # Load existing song ID mappings and external songs
    existing_mappings, external_songs = load_existing_mappings('songs_mapping.csv')
    print(f"Loaded {len(existing_mappings)} existing song ID(s) from CSV")
    print(f"Found {len(external_songs)} external link(s) in CSV\n")

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
        # Add html_filename and stable song_id to each file
        for file_info in files:
            # Check if this song already has an ID in the CSV
            key = (file_info['album'], file_info['title'], file_info['audio_url'])
            if key in existing_mappings:
                # Reuse existing ID
                file_info['song_id'] = existing_mappings[key]
            else:
                # Generate new stable ID
                file_info['song_id'] = generate_stable_id(
                    file_info['album'],
                    file_info['title'],
                    file_info['audio_url']
                )

            # Use song_id as the HTML filename for clean, stable URLs
            file_info['html_filename'] = f"{file_info['song_id']}.html"

        # Merge external songs with local files
        all_songs = files + external_songs
        print(f"\n✓ Total songs (local + external): {len(all_songs)}")

        # Save mappings to CSV
        save_mappings_to_csv(all_songs, 'songs_mapping.csv')

        output = {
            "files": all_songs,
            "count": len(all_songs)
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
