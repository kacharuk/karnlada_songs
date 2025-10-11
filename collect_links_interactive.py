#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive script to collect OneDrive share links for all songs.
This makes it easy to paste links one by one and automatically updates the configuration.
"""

import json
import os
import re
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Fixed values
ARTIST = "กาญจน์ลดา มฤคพิทักษ์"
ALBUM_ART_URL = "https://1drv.ms/i/c/19724284c9b34401/EaRNlSs0VH9IpgzboKat2vYBNdVlQ9a4WWOoIvvnracDrA?e=s9mA4Q"

def extract_title_from_filename(filepath):
    """Extract clean title from filename"""
    filename = os.path.basename(filepath)
    title = os.path.splitext(filename)[0]

    # Remove artist name suffixes
    title = re.sub(r' - กาญจน์ลดา มฤคพิทักษ์$', '', title)
    title = re.sub(r' ชรินทร์$', '', title)

    # Remove track numbers
    title = re.sub(r'^\d+\.\s*', '', title)

    return title.strip()

def convert_to_download_link(share_link):
    """Convert OneDrive share link to direct download/embed link"""
    share_link = share_link.strip()

    # If already a download link, return as-is
    if '/download?' in share_link:
        return share_link

    # For embedded players, we can use the share link directly
    # Or try to convert to download format

    # Extract components from 1drv.ms links
    if '1drv.ms' in share_link:
        # These links work for embedding/streaming
        return share_link

    # For onedrive.live.com links
    if 'onedrive.live.com' in share_link:
        # Try to convert to download
        if 'resid=' in share_link or '?id=' in share_link:
            # Add download parameter
            if '?' in share_link:
                return share_link + '&download=1'
            else:
                return share_link + '?download=1'

    return share_link

def load_song_list():
    """Load the list of songs from the text file"""
    songs_file = 'all_songs.txt'

    if not os.path.exists(songs_file):
        print("Error: all_songs.txt not found!")
        print("Please run: python scan_local_onedrive.py first")
        return []

    songs = []
    with open(songs_file, 'r', encoding='utf-8') as f:
        for line in f:
            filepath = line.strip()
            if filepath:
                title = extract_title_from_filename(filepath)
                songs.append({
                    'filepath': filepath,
                    'title': title
                })

    return songs

def load_existing_config():
    """Load existing configuration if available"""
    config_file = 'songs_config.json'

    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    return {'files': []}

def save_config(config):
    """Save configuration to JSON file"""
    with open('songs_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def update_list_file(files):
    """Update list_onedrive_files.py with the collected data"""
    # Generate the files array
    files_array = "    files = [\n"
    for file_info in files:
        files_array += f'''        {{
            "title": "{file_info['title']}",
            "artist": "{file_info['artist']}",
            "audio_url": "{file_info['audio_url']}",
            "album_art_url": "{file_info['album_art_url']}"
        }},\n'''
    files_array += "    ]"

    # Read the template
    with open('list_onedrive_files.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the files array
    pattern = r'files = \[.*?\]'
    new_content = re.sub(pattern, files_array, content, flags=re.DOTALL)

    # Save back
    with open('list_onedrive_files.py', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n[OK] Updated list_onedrive_files.py with {len(files)} songs")

def main():
    print("="*70)
    print(" " * 15 + "ONEDRIVE SHARE LINK COLLECTOR")
    print("="*70)
    print()

    # Load song list
    songs = load_song_list()

    if not songs:
        return

    print(f"Found {len(songs)} songs to process\n")

    # Load existing configuration
    config = load_existing_config()
    existing_files = {f['title']: f for f in config.get('files', [])}

    print("INSTRUCTIONS:")
    print("-" * 70)
    print("1. For each song, right-click the file in OneDrive folder")
    print("2. Select 'Share' -> 'Copy link'")
    print("3. Paste the link here")
    print("4. Press Enter to skip a song (can add later)")
    print("5. Type 'quit' to save and exit")
    print("-" * 70)
    print()

    collected_files = list(existing_files.values())
    new_count = 0
    skip_count = 0

    for idx, song in enumerate(songs, 1):
        title = song['title']

        # Check if already collected
        if title in existing_files:
            print(f"[{idx}/{len(songs)}] {title}")
            print(f"  [OK] Already configured")
            print()
            continue

        print(f"[{idx}/{len(songs)}] {title}")
        print(f"  File: {song['filepath']}")
        print("-" * 70)

        share_link = input("  Paste OneDrive share link (or Enter to skip, 'quit' to exit): ").strip()

        if share_link.lower() == 'quit':
            print("\nSaving progress...")
            break

        if not share_link:
            print("  [SKIP] Skipped")
            skip_count += 1
            print()
            continue

        # Convert to download link
        download_link = convert_to_download_link(share_link)

        # Add to configuration
        file_entry = {
            'title': title,
            'artist': ARTIST,
            'audio_url': download_link,
            'album_art_url': ALBUM_ART_URL
        }

        collected_files.append(file_entry)
        existing_files[title] = file_entry
        new_count += 1

        print(f"  [OK] Added ({new_count} new songs collected)")
        print()

        # Auto-save every 10 songs
        if new_count % 10 == 0:
            config['files'] = collected_files
            save_config(config)
            print(f"  [SAVE] Auto-saved ({len(collected_files)} total)")
            print()

    # Final save
    config['files'] = collected_files
    save_config(config)

    print("\n" + "="*70)
    print("COLLECTION SUMMARY")
    print("="*70)
    print(f"Total songs: {len(songs)}")
    print(f"Configured: {len(collected_files)}")
    print(f"New this session: {new_count}")
    print(f"Skipped: {skip_count}")
    print(f"Remaining: {len(songs) - len(collected_files)}")
    print()
    print(f"[OK] Configuration saved to: songs_config.json")

    if collected_files:
        print("\nDo you want to update list_onedrive_files.py now?")
        update = input("This will enable generating the HTML players (y/n): ").strip().lower()

        if update == 'y':
            update_list_file(collected_files)
            print("\n[OK] Configuration updated!")
            print("\nNext step: Run 'python run_all.py' to generate and deploy")
        else:
            print("\nYou can update later by running this script again")

    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[WARN] Interrupted by user. Progress has been saved.")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
