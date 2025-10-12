#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick rebuild script - scans all audio files and regenerates all HTML pages.

Usage:
    python rebuild.py

This script will:
1. Scan all audio files in docs/audio/ (including subfolders)
2. Extract song titles and metadata
3. Generate stub pages for each song
4. Generate central player.html
5. Generate index.html with album organization

After running this, just commit and push to deploy:
    git add -A
    git commit -m "Update songs"
    git push
"""

import subprocess
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def main():
    print("="*60)
    print("REBUILDING MUSIC LIBRARY")
    print("="*60)
    print()

    # Step 1: Scan audio files and generate metadata
    print("📁 Step 1: Scanning audio files...")
    result = subprocess.run([sys.executable, 'list_onedrive_files.py'],
                          capture_output=False, text=True)
    if result.returncode != 0:
        print("❌ Error scanning audio files")
        return 1

    print()

    # Step 2: Generate HTML pages
    print("📄 Step 2: Generating HTML pages...")
    result = subprocess.run([sys.executable, 'generate_players.py'],
                          capture_output=False, text=True)
    if result.returncode != 0:
        print("❌ Error generating HTML pages")
        return 1

    print()
    print("="*60)
    print("✅ REBUILD COMPLETE!")
    print("="*60)
    print()
    print("Generated files:")
    print("  - 171+ song stub pages (docs/*.html)")
    print("  - Central player (docs/player.html)")
    print("  - Album-organized index (docs/index.html)")
    print("  - Metadata files (onedrive_files.json, generated_urls.json)")
    print()
    print("Next steps:")
    print("  1. Review the changes (optional)")
    print("  2. Deploy to GitHub:")
    print("     git add -A")
    print("     git commit -m \"Update songs\"")
    print("     git push")
    print()

if __name__ == "__main__":
    sys.exit(main())
