#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix OneDrive links to use direct download/embed format
"""

import re

def convert_onedrive_to_embed(share_link):
    """
    Convert OneDrive share link to direct embed/download URL

    From: https://1drv.ms/u/c/CID/ENCODED_RESID?e=CODE
    To: https://onedrive.live.com/embed?resid=CID%21RESID&authkey=AUTHKEY
    """

    # Pattern for 1drv.ms links
    # Format: https://1drv.ms/u/c/19724284c9b34401/ENCODED?e=CODE

    if '1drv.ms' not in share_link:
        return share_link

    # Extract parts
    match = re.search(r'1drv\.ms/[a-z]/c/([^/]+)/([^?]+)', share_link)

    if not match:
        print(f"Could not parse: {share_link}")
        return share_link

    cid = match.group(1)
    encoded_part = match.group(2)

    # Decode the encoded part
    # The encoded part contains the resid
    # For audio files: /u/ or /a/ (audio)
    # For images: /i/ (image)

    # Try to construct embed URL
    # Format: https://onedrive.live.com/embed?resid=CID!RESID&authkey=!...

    print(f"\nOriginal: {share_link}")
    print(f"CID: {cid}")
    print(f"Encoded: {encoded_part}")

    # We need to get the actual RESID from the encoded part
    # The easiest way is to use download parameter

    # Alternative: Use download URL format
    if '/u/' in share_link or '/a/' in share_link:
        # Audio file - try download parameter
        download_url = share_link.replace('?', '&').replace('1drv.ms/u/', '1drv.ms/download/').replace('1drv.ms/a/', '1drv.ms/download/')
        download_url = 'https://api.onedrive.com/v1.0/shares/' + encoded_part + '/root/content'
        print(f"Could try: {download_url}")

    elif '/i/' in share_link:
        # Image file
        download_url = share_link.replace('?', '&').replace('1drv.ms/i/', '1drv.ms/download/')
        print(f"Could try: {download_url}")

    return share_link

# Test with your links
audio_link = "https://1drv.ms/u/c/19724284c9b34401/EQFEs8mEQnIggBlCYAYAAAABfVDhW3DjyPc_oTK-kEXueg?e=A9xNma"
image_link = "https://1drv.ms/i/c/19724284c9b34401/EaRNlSs0VH9IpgzboKat2vYBNdVlQ9a4WWOoIvvnracDrA?e=s9mA4Q"

print("="*70)
print("TESTING LINK CONVERSION")
print("="*70)

convert_onedrive_to_embed(audio_link)
print()
convert_onedrive_to_embed(image_link)

print("\n" + "="*70)
print("INSTRUCTIONS TO GET DIRECT LINKS:")
print("="*70)
print("""
The issue is that 1drv.ms links are preview links, not direct media links.

To get direct playable links:

METHOD 1 - Use Embed Links (RECOMMENDED):
1. Go to onedrive.live.com
2. Right-click your file
3. Click "Embed"
4. Copy the iframe src URL
5. That URL will work for direct playback

METHOD 2 - Use Download Links:
1. Right-click file in OneDrive web
2. Click "Download"
3. Copy the download link from browser
4. Use that URL

METHOD 3 - Manual URL Construction:
For your links, try these formats:

Audio (replace with your actual IDs):
https://onedrive.live.com/download?cid=19724284C9B34401&resid=19724284C9B34401%21XXXXX&authkey=!XXXXX

Image (for album art):
https://onedrive.live.com/download?cid=19724284C9B34401&resid=19724284C9B34401%21XXXXX&authkey=!XXXXX

Would you like me to create a web-based tool to help convert these links?
""")
