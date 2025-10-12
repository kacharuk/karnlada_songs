#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to scan for new audio files and update songs_mapping.csv
WITHOUT regenerating HTML pages.

Usage:
1. Copy new audio files to docs/audio/{album}/
2. Run: python scan_new_songs.py
3. Review and edit songs_mapping.csv (reorder, add external links, etc.)
4. Run: python rebuild.py to generate HTML pages
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
    Removes numbering prefix like "01", "02. ", etc.
    """
    # Remove extension
    name = os.path.splitext(filename)[0]

    # Remove numbering prefix (e.g., "01", "02.", "03. ", "04 ")
    import re
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

def generate_stable_id(album, title, audio_file_path):
    """
    Generate a stable ID for a song based on album + title + path.
    Uses a hash to create a short, stable identifier.
    """
    unique_string = f"{album}:{title}:{audio_file_path}"
    hash_object = hashlib.md5(unique_string.encode('utf-8'))
    return hash_object.hexdigest()[:8]

def load_existing_songs(csv_path='songs_mapping.csv'):
    """
    Load existing songs from CSV.
    Returns:
    - existing_songs: list of all song dicts
    - song_keys: set of (album, title, audio_path) for quick lookup
    """
    existing_songs = []
    song_keys = set()

    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_songs.append(row)
                key = (row['album'], row['title'], row['audio_file_path'])
                song_keys.add(key)

    return existing_songs, song_keys

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

def save_songs_to_csv(all_songs, csv_path='songs_mapping.csv'):
    """
    Save all songs to CSV file, preserving order from input list.
    """
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['song_id', 'album', 'title', 'artist', 'audio_file_path', 'html_filename', 'is_external']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for song in all_songs:
            writer.writerow({
                'song_id': song['song_id'],
                'album': song['album'],
                'title': song['title'],
                'artist': song['artist'],
                'audio_file_path': song.get('audio_url', song.get('audio_file_path', '')),
                'html_filename': song['html_filename'],
                'is_external': song.get('is_external', 'false')
            })

    print(f"✓ Saved {len(all_songs)} songs to: {csv_path}")

def main():
    print("="*60)
    print("SCANNING FOR NEW SONGS")
    print("="*60)
    print()

    # Load existing songs from CSV
    existing_songs, existing_keys = load_existing_songs('songs_mapping.csv')
    print(f"📋 Loaded {len(existing_songs)} existing song(s) from CSV\n")

    # Scan audio folders for all files
    scanned_files = scan_audio_folders('docs/audio')

    if not scanned_files:
        print("\n" + "="*60)
        print("No audio files found in docs/audio/")
        print("="*60)
        return

    # Find new songs that aren't in CSV yet
    new_songs = []
    for file_info in scanned_files:
        key = (file_info['album'], file_info['title'], file_info['audio_url'])
        if key not in existing_keys:
            new_songs.append(file_info)

    print("="*60)
    print(f"SCAN RESULTS")
    print("="*60)
    print(f"Total files scanned:     {len(scanned_files)}")
    print(f"Existing songs in CSV:   {len(existing_songs)}")
    print(f"New songs found:         {len(new_songs)}")
    print("="*60)

    # Generate IDs and metadata for new songs
    new_entries = []
    if new_songs:
        print(f"\n📝 Adding {len(new_songs)} new song(s):\n")
    else:
        print("\n✅ No new songs to add. CSV is up to date!")
    for file_info in new_songs:
        # Generate stable ID
        song_id = generate_stable_id(
            file_info['album'],
            file_info['title'],
            file_info['audio_url']
        )

        entry = {
            'song_id': song_id,
            'album': file_info['album'],
            'title': file_info['title'],
            'artist': file_info['artist'],
            'audio_url': file_info['audio_url'],
            'html_filename': f"{song_id}.html",
            'is_external': 'false',
            'album_art_url': file_info['album_art_url']
        }
        new_entries.append(entry)
        print(f"  + [{song_id}] {file_info['album']} - {file_info['title']}")

    # Append new songs to existing songs list
    # Convert existing CSV rows to same format as new entries
    all_songs = []
    for row in existing_songs:
        all_songs.append({
            'song_id': row['song_id'],
            'album': row['album'],
            'title': row['title'],
            'artist': row['artist'],
            'audio_url': row['audio_file_path'],
            'html_filename': row['html_filename'],
            'is_external': row.get('is_external', 'false'),
            'album_art_url': ''  # Not stored in CSV
        })

    # Add new songs at the end
    all_songs.extend(new_entries)

    # Save updated CSV
    print()
    save_songs_to_csv(all_songs, 'songs_mapping.csv')

    print("\n" + "="*60)
    print("✅ SCAN COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review songs_mapping.csv")
    print("   - Reorder songs if needed")
    print("   - Add external links (set is_external=true)")
    print("   - Update titles or artist names")
    print()
    print("2. Run: python rebuild.py")
    print("   - Generates HTML pages for all songs")
    print("   - Updates index.html")
    print()

if __name__ == "__main__":
    main()
