#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatically fix OneDrive links to use direct embed/download URLs
"""

import re
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def convert_1drv_to_embed(url):
    """
    Convert 1drv.ms URLs to OneDrive embed format that works with HTML5 audio/img

    From: https://1drv.ms/u/c/19724284c9b34401/EQFEs8mEQnIggBlCYAYAAAABfVDhW3DjyPc_oTK-kEXueg?e=A9xNma
    To: https://api.onedrive.com/v1.0/shares/u!{share_token}/root/content
    """

    if '1drv.ms' not in url:
        return url

    # Extract share token (the encoded part after the CID)
    match = re.search(r'1drv\.ms/[a-z]/c/[^/]+/([^?]+)', url)
    if not match:
        return url

    share_token = match.group(1)

    # Use OneDrive API to get direct content
    # This format works for both audio and images
    new_url = f"https://api.onedrive.com/v1.0/shares/u!{share_token}/root/content"

    return new_url

def fix_file():
    """
    Read list_onedrive_files.py and fix all OneDrive URLs
    """

    file_path = 'list_onedrive_files.py'

    print("="*70)
    print("AUTO-FIX ONEDRIVE LINKS")
    print("="*70)
    print()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return False

    original_content = content
    replacements = 0

    # Find all 1drv.ms URLs
    def replacer(match):
        nonlocal replacements
        old_url = match.group(0)
        new_url = convert_1drv_to_embed(old_url)

        if new_url != old_url:
            replacements += 1
            print(f"[{replacements}] Converting:")
            print(f"  FROM: {old_url}")
            print(f"  TO:   {new_url}")
            print()

        return new_url

    # Replace all 1drv.ms URLs
    content = re.sub(r'https://1drv\.ms/[^\s"\']+', replacer, content)

    if content == original_content:
        print("[INFO] No 1drv.ms links found to convert")
        return False

    # Backup original
    backup_path = 'list_onedrive_files.py.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"[OK] Backup saved to: {backup_path}")

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Updated {replacements} URLs in: {file_path}")

    return True

def main():
    print("\nThis script will automatically convert all 1drv.ms links")
    print("to API URLs that work with HTML5 audio and img tags.\n")

    proceed = input("Proceed? (y/n): ").strip().lower()

    if proceed != 'y':
        print("Cancelled.")
        return

    print()
    success = fix_file()

    if success:
        print("\n" + "="*70)
        print("LINKS UPDATED SUCCESSFULLY!")
        print("="*70)
        print("\nNext steps:")
        print("1. python generate_players.py   # Regenerate HTML files")
        print("2. git add . && git commit -m 'Fix OneDrive links for direct playback' && git push")
        print("3. Wait 2-3 minutes for GitHub Pages")
        print("4. Test your players!")
        print("\nNote: If audio/image still don't load, you may need to get")
        print("proper embed URLs from OneDrive web interface.")
    else:
        print("\n[INFO] No changes made")

    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
