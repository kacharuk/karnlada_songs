#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert OneDrive embed URLs to download URLs
"""

import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def convert_to_download_url(embed_url):
    """
    Try converting OneDrive embed URL to download format

    From: https://1drv.ms/u/c/19724284c9b34401/IQQBRLPJhEJyIIAZQmAGAAAAARcbHvVJiGHTnxmtDnP6qL8
    To: https://onedrive.live.com/download?resid=19724284C9B34401%21RESID&authkey=...
    """

    if '1drv.ms' not in embed_url:
        return embed_url

    # Extract CID and encoded RESID
    parts = embed_url.split('/')

    # Find CID (the long hex number)
    cid = None
    encoded_resid = None

    for i, part in enumerate(parts):
        if len(part) == 16 and all(c in '0123456789abcdefABCDEF' for c in part):
            cid = part.upper()
            if i + 1 < len(parts):
                encoded_resid = parts[i + 1]
            break

    if not cid or not encoded_resid:
        print(f"Could not parse: {embed_url}")
        return embed_url

    # Try different download URL formats
    formats = [
        # Format 1: Direct download parameter
        f"{embed_url}?download=1",

        # Format 2: Add /download endpoint
        embed_url.replace('/u/', '/download/').replace('/i/', '/download/'),

        # Format 3: Use e1.onedrive.com (content delivery network)
        f"https://e1.onedrive.com/share/s!{encoded_resid}",

        # Format 4: Construct download URL
        f"https://onedrive.live.com/download?cid={cid}&resid={encoded_resid}",
    ]

    return formats

# Test with your URLs
audio_embed = "https://1drv.ms/u/c/19724284c9b34401/IQQBRLPJhEJyIIAZQmAGAAAAARcbHvVJiGHTnxmtDnP6qL8"
image_embed = "https://1drv.ms/i/c/19724284c9b34401/IQSkTZUrNFR_SKYM26Cmrdr2AdHBzIc38awev5p0SsMzgtQ"

print("="*70)
print("TRYING DIFFERENT URL FORMATS")
print("="*70)

print("\nAUDIO FILE:")
print(f"Original: {audio_embed}")
print("\nTry these URLs:")
for idx, url in enumerate(convert_to_download_url(audio_embed), 1):
    print(f"  {idx}. {url}")

print("\n" + "-"*70)

print("\nIMAGE FILE:")
print(f"Original: {image_embed}")
print("\nTry these URLs:")
for idx, url in enumerate(convert_to_download_url(image_embed), 1):
    print(f"  {idx}. {url}")

print("\n" + "="*70)
print("RECOMMENDED APPROACH:")
print("="*70)
print("""
Since OneDrive embed URLs don't work directly, try this:

1. Open onedrive.live.com
2. Right-click file → Download
3. Open DevTools (F12) → Network tab
4. Look for the actual download URL in the network requests
5. Copy that URL (will look like public.am.files.1drv.com/...)
6. Use that direct URL instead

That's the only guaranteed way to get working direct media URLs.
""")
