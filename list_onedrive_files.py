#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to list OneDrive files and their public access links.
Creates a JSON file with all the music file information.
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

def get_onedrive_files():
    """
    This function needs to be customized with your OneDrive shared links.

    For each music file, you need to provide:
    - title: Song title
    - artist: Artist/singer name
    - audio_url: OneDrive public share link for the audio file (mp3 or m4a)
    - album_art_url: OneDrive public share link for the album art image
    """

    # Template for adding your files
    files = [
        {
            "title": "กระซิบสวาท",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/กระซิบสวาท - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "กล้วยไม้",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/กล้วยไม้ - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "กว่าเราจะรักกันได้",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/กว่าเราจะรักกันได้ - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "ขวัญเรียม",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/ขวัญเรียม - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "ขอรักคืน",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/ขอรักคืน - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "คนึงครวญ",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/คนึงครวญ - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "ดอกไม้กับเพลง",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/ดอกไม้กับเพลง - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "ดอกไม้ใกล้มือ",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/ดอกไม้ใกล้มือ - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "ถึงเธอ",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/ถึงเธอ - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
        {
            "title": "บัวกลางบึง",
            "artist": "กาญจน์ลดา มฤคพิทักษ์",
            "audio_url": "audio/บัวกลางบึง - กาญจน์ลดา มฤคพิทักษ์.mp3",
            "album_art_url": "images/album_art_karnlada.jpg"
        },
    ]

    return files

def convert_onedrive_link(share_link):
    """
    Convert OneDrive sharing link to direct download link.

    If you have a OneDrive share link like:
    https://onedrive.live.com/?id=ABC123...

    You need to convert it to a direct download link.
    """
    if 'download?' in share_link:
        return share_link

    # If it's a view link, try to convert to download
    if 'onedrive.live.com' in share_link:
        print(f"Note: Link might need manual conversion: {share_link}")
        print("To get direct download links:")
        print("1. Right-click file in OneDrive > Share")
        print("2. Click 'Copy link' and ensure 'Anyone with the link can view' is set")
        print("3. Use the embed option or modify the link to use /download endpoint")

    return share_link

def main():
    print("Fetching OneDrive file information...")

    files = get_onedrive_files()

    if not files:
        print("\n" + "="*60)
        print("No files configured yet!")
        print("="*60)
        print("\nPlease edit list_onedrive_files.py and add your music files.")
        print("\nFor each file, you need:")
        print("  1. Song title")
        print("  2. Artist name")
        print("  3. OneDrive public link for audio file (mp3/m4a)")
        print("  4. OneDrive public link for album art image")
        print("\nHow to get OneDrive public links:")
        print("  1. Right-click file in OneDrive")
        print("  2. Click 'Share' > 'Copy link'")
        print("  3. Make sure 'Anyone with the link can view' is selected")
        print("  4. For direct playback, use the embed/download URL format")
        print("="*60)

        # Create empty output file
        output = {
            "files": [],
            "count": 0
        }
    else:
        # Validate and process links
        for file_info in files:
            file_info['audio_url'] = convert_onedrive_link(file_info['audio_url'])
            file_info['album_art_url'] = convert_onedrive_link(file_info['album_art_url'])

            # Generate a safe filename for the HTML file
            safe_title = "".join(c for c in file_info['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_').lower()
            file_info['html_filename'] = f"{safe_title}.html"

        output = {
            "files": files,
            "count": len(files)
        }

        print(f"\nFound {len(files)} music file(s)")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file['title']} - {file['artist']}")

    # Save to JSON file
    output_file = 'onedrive_files.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nOutput saved to: {output_file}")
    return output

if __name__ == "__main__":
    main()
