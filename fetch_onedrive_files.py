#!/usr/bin/env python3
"""
Script to fetch files from a OneDrive shared folder using Microsoft Graph API.
This script extracts the shared folder URL and lists all MP3/M4A files with their download links.
"""

import requests
import json
import re
from urllib.parse import parse_qs, urlparse, unquote

def extract_share_info(share_url):
    """
    Extract the resource ID and CID from OneDrive share URL.
    """
    # Parse the URL
    if '1drv.ms' in share_url:
        # This is a shortened link, we need to extract from the full redirect
        # The URL format: https://1drv.ms/f/c/CID/RESID_INFO
        parts = share_url.split('/f/c/')
        if len(parts) > 1:
            path_parts = parts[1].split('/')
            if len(path_parts) > 1:
                cid = path_parts[0]
                # Extract resid from the encoded part
                encoded_part = path_parts[1]
                return cid, encoded_part

    # Try to extract from onedrive.live.com URL
    parsed = urlparse(share_url)
    query_params = parse_qs(parsed.query)

    cid = query_params.get('cid', [None])[0]
    resid = query_params.get('resid', [None])[0]

    return cid, resid

def get_sharing_link_info(share_url):
    """
    Use Microsoft Graph API to get folder contents from a sharing link.
    This uses the public API that doesn't require authentication for public shares.
    """

    # Extract share token from URL
    # For your URL: https://1drv.ms/f/c/19724284c9b34401/EgFEs8mEQnIggBlfigAAAAAB8rdh_eHfc8HBL-q-jBvY8Q

    print("Analyzing share URL...")
    print(f"URL: {share_url}\n")

    # Method 1: Try to use the share link directly with Graph API
    # Encode the sharing URL as a share token
    import base64

    # The sharing URL needs to be base64 encoded for Graph API
    encoded_url = base64.b64encode(share_url.encode()).decode()
    # Remove padding and replace characters for URL-safe base64
    encoded_url = encoded_url.rstrip('=').replace('+', '-').replace('/', '_')

    # Graph API endpoint for shared items
    graph_url = f"https://graph.microsoft.com/v1.0/shares/u!{encoded_url}/root/children"

    print("Attempting to access via Microsoft Graph API...")
    print(f"Endpoint: {graph_url}\n")

    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get(graph_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Graph API returned status code: {response.status_code}")
            print(f"Response: {response.text}\n")
            return None
    except Exception as e:
        print(f"Error accessing Graph API: {e}\n")
        return None

def extract_from_embed_url(share_url):
    """
    Try to construct an embed URL and extract file information.
    """
    print("Trying alternative method using OneDrive embed API...\n")

    # Extract CID and RESID from your URL
    cid = "19724284c9b34401"
    resid = "19724284C9B34401!35423"

    # Construct the OneDrive embed API URL
    embed_url = f"https://onedrive.live.com/embed?cid={cid}&resid={resid}&authkey=!AESzySMCciCAGV-I"

    print(f"Embed URL: {embed_url}")
    print("\nNote: This method may require browser-based access.\n")

    return None

def manual_link_generator(cid, resid_base, file_list):
    """
    Generate download links for files based on OneDrive structure.
    """
    download_links = []

    for file_info in file_list:
        filename = file_info['name']
        # Construct download URL
        # Format: https://onedrive.live.com/download?cid=CID&resid=RESID&authkey=AUTHKEY
        download_url = f"https://onedrive.live.com/download?cid={cid}&resid={resid_base}_{file_info['id']}&authkey=!AESzySMCciCAGV-I"

        download_links.append({
            'filename': filename,
            'download_url': download_url
        })

    return download_links

def main():
    print("="*60)
    print("ONEDRIVE FILE FETCHER")
    print("="*60)
    print()

    # Your OneDrive share URL
    share_url = "https://1drv.ms/f/c/19724284c9b34401/EgFEs8mEQnIggBlfigAAAAAB8rdh_eHfc8HBL-q-jBvY8Q?e=EyXnGz"

    # Try Graph API method
    data = get_sharing_link_info(share_url)

    if data and 'value' in data:
        print("✓ Successfully retrieved folder contents!\n")
        files = data['value']

        # Filter for audio files
        audio_files = [f for f in files if f['name'].lower().endswith(('.mp3', '.m4a'))]
        image_files = [f for f in files if f['name'].lower().endswith(('.jpg', '.jpeg', '.png'))]

        print(f"Found {len(audio_files)} audio files")
        print(f"Found {len(image_files)} image files\n")

        print("Audio Files:")
        print("-" * 60)
        for f in audio_files:
            print(f"  - {f['name']} ({f.get('size', 'unknown')} bytes)")
            if '@microsoft.graph.downloadUrl' in f:
                print(f"    Download: {f['@microsoft.graph.downloadUrl'][:80]}...")

        print("\nImage Files:")
        print("-" * 60)
        for f in image_files:
            print(f"  - {f['name']}")

        # Save to JSON
        output = {
            'audio_files': audio_files,
            'image_files': image_files
        }

        with open('onedrive_raw_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Raw data saved to: onedrive_raw_data.json")
        return True

    else:
        print("❌ Could not access folder via Graph API.")
        print("\nThis might be because:")
        print("1. The folder requires authentication")
        print("2. Microsoft Graph API needs app registration")
        print("3. The share link format needs special handling\n")

        print("ALTERNATIVE APPROACH:")
        print("="*60)
        print("\nI'll create a helper script that you can use to manually")
        print("input the file information, which might be easier.\n")

        return False

if __name__ == "__main__":
    success = main()

    if not success:
        print("\nNext steps:")
        print("1. Open your OneDrive folder in a browser")
        print("2. Use the manual helper script (coming next)")
        print("3. Or we can set up proper Graph API authentication")
