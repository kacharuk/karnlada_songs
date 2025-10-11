#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch import OneDrive links from a file.
Useful if you've already copied all share links to a text file.
"""

import json
import os
import re
from collect_links_interactive import (
    ARTIST, ALBUM_ART_URL,
    extract_title_from_filename,
    convert_to_download_link,
    load_song_list,
    save_config,
    update_list_file
)

def import_from_file(links_file):
    """Import links from a text file where each line is a share link"""

    if not os.path.exists(links_file):
        print(f"Error: {links_file} not found!")
        print("\nCreate a text file with one OneDrive share link per line,")
        print("in the same order as the songs in all_songs.txt")
        return

    # Load songs
    songs = load_song_list()
    if not songs:
        return

    # Load links
    with open(links_file, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]

    print(f"Found {len(songs)} songs")
    print(f"Found {len(links)} links")

    if len(links) != len(songs):
        print("\nWarning: Number of links doesn't match number of songs!")
        print("Proceeding with minimum count...")

    # Create configuration
    files = []
    count = min(len(songs), len(links))

    for i in range(count):
        song = songs[i]
        link = links[i]

        download_link = convert_to_download_link(link)

        files.append({
            'title': song['title'],
            'artist': ARTIST,
            'audio_url': download_link,
            'album_art_url': ALBUM_ART_URL
        })

        print(f"[{i+1}/{count}] {song['title']}")

    # Save configuration
    config = {'files': files}
    save_config(config)

    print(f"\n[OK] Saved {len(files)} songs to songs_config.json")

    # Ask to update list file
    update = input("\nUpdate list_onedrive_files.py? (y/n): ").strip().lower()
    if update == 'y':
        update_list_file(files)
        print("\n[OK] Configuration updated!")
        print("Next step: Run 'python run_all.py'")

if __name__ == "__main__":
    print("="*70)
    print("BATCH IMPORT ONEDRIVE LINKS")
    print("="*70)
    print()
    print("This script imports links from a text file (one link per line)")
    print()

    links_file = input("Enter path to links file (or press Enter for 'links.txt'): ").strip()
    if not links_file:
        links_file = 'links.txt'

    import_from_file(links_file)
