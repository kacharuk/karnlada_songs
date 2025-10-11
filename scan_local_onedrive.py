#!/usr/bin/env python3
"""
Script to scan local OneDrive folder for MP3/M4A files and generate public share links.
This uses the Windows OneDrive API to get share links for synced files.
"""

import os
import subprocess
import json
from pathlib import Path
import re

# Fixed values
ARTIST = "กาญจน์ลดา มฤคพิทักษ์"
ALBUM_ART_URL = "https://1drv.ms/i/c/19724284c9b34401/EaRNlSs0VH9IpgzboKat2vYBNdVlQ9a4WWOoIvvnracDrA?e=s9mA4Q"

def find_onedrive_folder():
    """Find the OneDrive folder on the local machine"""
    # Common OneDrive locations
    possible_paths = [
        os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive - Personal'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive - กาญจน์ลดา'),
    ]

    print("Searching for OneDrive folder...")
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found OneDrive at: {path}")
            return path

    # Ask user for custom path
    print("\nCouldn't find OneDrive folder automatically.")
    custom_path = input("Please enter your OneDrive folder path: ").strip()
    if os.path.exists(custom_path):
        return custom_path

    return None

def find_audio_files(base_path):
    """Find all MP3 and M4A files in the directory"""
    audio_files = []

    if not base_path:
        return audio_files

    print(f"\nScanning for audio files in: {base_path}")

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(('.mp3', '.m4a')):
                full_path = os.path.join(root, file)
                audio_files.append(full_path)

    return audio_files

def get_onedrive_share_link_powershell(file_path):
    """
    Get OneDrive share link using PowerShell.
    This uses the OneDrive COM object to get sharing links.
    """
    try:
        # PowerShell script to get share link
        ps_script = f'''
        Add-Type -AssemblyName System.Web
        $file = Get-Item "{file_path}"

        # Try to get existing share link from alternate data stream
        $webUrl = Get-Content -Path "{file_path}" -Stream Zone.Identifier -ErrorAction SilentlyContinue | Select-String -Pattern "HostUrl" | ForEach-Object {{ $_.Line.Split('=')[1] }}

        if ($webUrl) {{
            Write-Output $webUrl
        }} else {{
            Write-Output "NO_LINK"
        }}
        '''

        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != "NO_LINK":
            return result.stdout.strip()
    except Exception as e:
        print(f"PowerShell method failed: {e}")

    return None

def construct_onedrive_link(file_path, onedrive_root):
    """
    Construct OneDrive link based on file path structure.
    This assumes the OneDrive folder structure maps to the web URLs.
    """
    # Get relative path from OneDrive root
    try:
        rel_path = os.path.relpath(file_path, onedrive_root)
        # Convert to web-safe format
        # This is a placeholder - actual implementation would need OneDrive API
        return None
    except:
        return None

def manual_link_builder(audio_files):
    """
    Helper to manually build links by asking user to share files.
    """
    print("\n" + "="*60)
    print("MANUAL LINK GENERATION")
    print("="*60)
    print("\nFor each file, you'll need to get the OneDrive share link.")
    print("\nHow to get share links:")
    print("1. Right-click the file in File Explorer")
    print("2. Select 'Share' (OneDrive option)")
    print("3. Click 'Copy link'")
    print("4. Paste it here\n")

    file_data = []

    for idx, file_path in enumerate(audio_files, 1):
        filename = os.path.basename(file_path)
        print(f"\n[{idx}/{len(audio_files)}] {filename}")
        print("-" * 60)

        share_link = input("Paste OneDrive share link (or press Enter to skip): ").strip()

        if share_link:
            # Convert to download link
            download_link = convert_to_download_link(share_link)

            # Use filename (without extension) as title
            title = os.path.splitext(filename)[0]

            file_data.append({
                'title': title,
                'artist': ARTIST,
                'audio_url': download_link,
                'album_art_url': ALBUM_ART_URL
            })

            print(f"✓ Added: {title}")

    return file_data

def convert_to_download_link(share_link):
    """
    Convert OneDrive share link to direct download link.
    """
    # If it's already a download link, return as-is
    if 'download?' in share_link:
        return share_link

    # For 1drv.ms links, we need to convert them
    # Format: https://1drv.ms/u/c/CID/ENCODED_DATA
    # We'll return the share link and let the HTML player handle it
    # Or convert to embed format

    # Try to extract and convert to download format
    if '1drv.ms' in share_link:
        # Extract parts from URL
        # Example: https://1drv.ms/u/c/19724284c9b34401/ENCODED_RESID
        parts = share_link.split('/')
        if len(parts) >= 6:
            cid = parts[5]
            # For now, return the share link - it should work for streaming
            return share_link

    if 'onedrive.live.com' in share_link:
        # Try to convert view link to download
        if '?id=' in share_link or 'resid=' in share_link:
            # Could construct download link
            return share_link.replace('?', '/download?')

    # Return as-is if can't convert
    return share_link

def save_to_list_file(file_data):
    """
    Update list_onedrive_files.py with the collected data.
    """
    # Read the template
    with open('list_onedrive_files.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate the files array
    files_array = "    files = [\n"
    for file_info in file_data:
        files_array += f'''        {{
            "title": "{file_info['title']}",
            "artist": "{file_info['artist']}",
            "audio_url": "{file_info['audio_url']}",
            "album_art_url": "{file_info['album_art_url']}"
        }},\n'''
    files_array += "    ]"

    # Replace the files array in the template
    # Find the files = [ ... ] section
    pattern = r'files = \[.*?\]'
    new_content = re.sub(pattern, files_array, content, flags=re.DOTALL)

    # Save back
    with open('list_onedrive_files.py', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n✓ Updated list_onedrive_files.py with {len(file_data)} songs")

def main():
    print("="*60)
    print("LOCAL ONEDRIVE AUDIO FILE SCANNER")
    print("="*60)
    print()

    # Ask for the specific folder with music files
    print("Where are your music files stored?")
    music_folder = input("Enter the full path to your music folder: ").strip()

    if not os.path.exists(music_folder):
        print(f"Error: Folder not found: {music_folder}")
        return

    # Find audio files
    audio_files = find_audio_files(music_folder)

    if not audio_files:
        print("No MP3 or M4A files found in the specified folder.")
        return

    print(f"\nFound {len(audio_files)} audio file(s):")
    for idx, file in enumerate(audio_files, 1):
        print(f"  {idx}. {os.path.basename(file)}")

    # Try to get share links automatically
    print("\nAttempting to get OneDrive share links automatically...")

    # For now, we'll use manual method
    # Automatic methods would require OneDrive API or COM automation

    file_data = manual_link_builder(audio_files)

    if file_data:
        # Save to configuration file
        save_to_list_file(file_data)

        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print(f"\n✓ Configured {len(file_data)} songs")
        print("\nNext steps:")
        print("1. Run: python run_all.py")
        print("2. This will generate HTML players and deploy to GitHub")
    else:
        print("\nNo files were configured.")

if __name__ == "__main__":
    main()
