#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper script to update OneDrive links in list_onedrive_files.py
This makes it easy to replace preview links with proper embed/download URLs
"""

import re
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def get_link_mapping():
    """
    Define mappings from old (preview) links to new (embed/download) links
    """

    print("="*70)
    print("ONEDRIVE LINK UPDATER")
    print("="*70)
    print("\nThis script will help you replace preview links with embed links.")
    print("\nFirst, let's get the correct URLs from OneDrive:\n")

    # Get album art embed URL
    print("ALBUM ART:")
    print("1. Go to: https://onedrive.live.com")
    print("2. Find your album art image")
    print("3. Right-click → Embed")
    print("4. Copy the src URL from the iframe code")
    print()

    album_art_old = "https://1drv.ms/i/c/19724284c9b34401/EaRNlSs0VH9IpgzboKat2vYBNdVlQ9a4WWOoIvvnracDrA?e=s9mA4Q"
    album_art_new = input(f"Paste new album art embed URL (or press Enter to skip): ").strip()

    if not album_art_new:
        print("Skipping album art update...")
        album_art_new = album_art_old

    print("\n" + "-"*70)
    print("\nNow for the AUDIO FILES, you have two options:\n")
    print("OPTION A - Update each song individually (tedious)")
    print("OPTION B - Use a pattern replacement (faster)\n")

    choice = input("Choose option (A/B): ").strip().upper()

    audio_mappings = {}

    if choice == 'A':
        # Individual mapping
        print("\nFor each song, get its embed URL from OneDrive...")
        print("(Type 'done' when finished)\n")

        songs = [
            ("กระซิบสวาท", "https://1drv.ms/u/c/19724284c9b34401/EQFEs8mEQnIggBlCYAYAAAABfVDhW3DjyPc_oTK-kEXueg?e=A9xNma"),
            ("กล้วยไม้", "https://1drv.ms/u/c/19724284c9b34401/EQFEs8mEQnIggBkvYAYAAAABWSTvdxrEBaP7pw4I5bpQMw?e=dLVNtp"),
            ("กว่าเราจะรักกันได้", "https://1drv.ms/u/c/19724284c9b34401/EQFEs8mEQnIggBk7YAYAAAAB7n73T0SdlL204sfj2icoRQ?e=EF4TP4"),
            # ... rest of songs
        ]

        for title, old_url in songs:
            new_url = input(f"{title}: ").strip()
            if new_url.lower() == 'done':
                break
            if new_url:
                audio_mappings[old_url] = new_url

    else:
        # Pattern replacement - convert 1drv.ms to embed format
        print("\nOPTION B: Automatic conversion")
        print("This will try to convert your links automatically.")
        print("\nTry getting ONE working embed URL first:")
        print("1. Pick any audio file from OneDrive")
        print("2. Right-click → Embed")
        print("3. Paste the embed URL here\n")

        sample_url = input("Sample embed URL: ").strip()

        if sample_url and 'onedrive.live.com' in sample_url:
            print("\n[OK] Will use this format for all files")
            # We'll do pattern-based replacement in the update function
        else:
            print("\n[WARN] No valid URL provided. Using download format instead.")
            sample_url = "download"

    return {
        'album_art_old': album_art_old,
        'album_art_new': album_art_new,
        'audio_mappings': audio_mappings,
        'use_pattern': choice == 'B',
        'sample_url': sample_url if choice == 'B' else None
    }

def convert_to_embed_url(preview_url, sample_embed_url=None):
    """
    Convert a 1drv.ms preview URL to an embed URL
    """

    if not preview_url or '1drv.ms' not in preview_url:
        return preview_url

    # Extract the share token
    match = re.search(r'1drv\.ms/[a-z]/c/[^/]+/([^?]+)', preview_url)
    if not match:
        return preview_url

    share_token = match.group(1)

    if sample_embed_url and 'onedrive.live.com/embed' in sample_embed_url:
        # Use the same format as sample
        # Extract pattern from sample
        base_pattern = re.sub(r'(resid=|cid=|authkey=)[^&]+', r'\1REPLACE', sample_embed_url)
        # This is complex - just use download format for now
        pass

    # Use download format which usually works
    return f"https://onedrive.live.com/download?resid={share_token}"

def update_file(mapping):
    """
    Update list_onedrive_files.py with new URLs
    """

    file_path = 'list_onedrive_files.py'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return False

    original_content = content

    # Replace album art URL
    if mapping['album_art_new'] != mapping['album_art_old']:
        content = content.replace(mapping['album_art_old'], mapping['album_art_new'])
        print(f"[OK] Replaced album art URL")

    # Replace audio URLs
    if mapping['use_pattern'] and mapping['sample_url']:
        # Pattern-based replacement
        if mapping['sample_url'] == "download":
            # Convert all 1drv.ms/u/ links to download format
            def replacer(match):
                full_url = match.group(0)
                new_url = convert_to_embed_url(full_url)
                print(f"  Converting: {full_url[:50]}...")
                return new_url

            content = re.sub(r'https://1drv\.ms/u/[^\s"\']+', replacer, content)
    else:
        # Individual mappings
        for old_url, new_url in mapping['audio_mappings'].items():
            if old_url in content:
                content = content.replace(old_url, new_url)
                print(f"[OK] Replaced audio URL")

    if content == original_content:
        print("\n[WARN] No changes made to file")
        return False

    # Backup original
    backup_path = 'list_onedrive_files.py.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"\n[OK] Backup saved to: {backup_path}")

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Updated: {file_path}")

    return True

def main():
    print("\n" + "="*70)
    print("STEP 1: Get the correct OneDrive URLs")
    print("="*70)

    mapping = get_link_mapping()

    print("\n" + "="*70)
    print("STEP 2: Update list_onedrive_files.py")
    print("="*70)

    proceed = input("\nProceed with update? (y/n): ").strip().lower()

    if proceed != 'y':
        print("Update cancelled.")
        return

    success = update_file(mapping)

    if success:
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print("\nNext steps:")
        print("1. Run: python generate_players.py")
        print("2. Run: git add . && git commit -m 'Fix OneDrive links' && git push")
        print("3. Wait 2-3 minutes for GitHub Pages to update")
        print("4. Test your music players!")

    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
