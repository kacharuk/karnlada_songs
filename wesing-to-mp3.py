#!/usr/bin/env python3
import os
import sys
import requests
from bs4 import BeautifulSoup
import subprocess
import json
import re
import shutil

# --- utility functions -----------------------------------------------------

def unique_filename(base, ext):
    """Return a filename that doesn't conflict by appending a suffix.

    base: filename without extension or path (can include directories)
    ext: extension including the leading dot (e.g. ".mp3")
    """
    candidate = f"{base}{ext}"
    counter = 2
    while os.path.exists(candidate):
        candidate = f"{base}-{counter}{ext}"
        counter += 1
    return candidate

# ----- ffmpeg helpers borrowed from convert_to_mp3.py ---------------------

FFMPEG_PATH = r"C:\tools\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\tools\ffmpeg\bin\ffprobe.exe"


def is_mp3(file_path):
    """Return True if the file is actually an MP3 according to ffprobe."""
    try:
        result = subprocess.run([
            FFPROBE_PATH,
            '-v', 'error',
            '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ], capture_output=True, text=True)
        return result.stdout.strip() == 'mp3'
    except subprocess.CalledProcessError:
        return False


def convert_to_mp3(input_path, output_path, bitrate='128k'):
    """Convert an audio file to MP3 using ffmpeg.

    Returns True on success, False otherwise.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        subprocess.run([
            FFMPEG_PATH,
            '-i', input_path,
            '-codec:a', 'libmp3lame',
            '-b:a', bitrate,
            '-map_metadata', '0',
            '-y',
            output_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e}")
        return False

# --------------------------------------------------------------------------

OUTPUT_DIR = "output"
MP3_DIR = os.path.join(OUTPUT_DIR, "mp3")

# create folders upfront
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MP3_DIR, exist_ok=True)

# helper to extract first URL from a line
def extract_url(line):
    """Return the first http(s) URL found in line, or None."""
    m = re.search(r'https?://[^\s\)\]\>,"]+', line)
    if not m:
        return None
    url = m.group(0).rstrip('.,;:)")\'')
    return url

# read URL list and extract URLs from each line (skip non-URL lines)
with open("list.txt", "r", encoding="utf-8") as f:
    urls = []
    for raw in f:
        line = raw.strip()
        if not line:
            continue
        url = extract_url(line)
        if url:
            urls.append(url)
        else:
            print(f"Skipping line without URL: {line}")

counter = 0

for url in urls:
    counter += 1
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", text=lambda t: t and "window.__DATA__" in t)
    if not script_tag:
        print(f"No script tag with audio data found in {url}")
        continue

    try:
        match = re.search(r"window\.__DATA__\s*=\s*(\{.*?\});", script_tag.string, re.DOTALL)
        if not match:
            raise ValueError("JSON data not found in script tag")

        data = json.loads(match.group(1))
        audio_src = data["detail"].get("playurl")
        if not audio_src:
            print(f"No audio source found for {url}")
            raise ValueError("playurl missing")

        audio_title = data["detail"]["song_name"].replace("/", "-").replace(":", "-")
        audio_path = unique_filename(os.path.join(OUTPUT_DIR, audio_title), ".m4a")
        mp3_path = unique_filename(os.path.join(MP3_DIR, audio_title), ".mp3")

    except (KeyError, IndexError, json.JSONDecodeError, ValueError) as e:
        print(f"Failed to extract audio data from {url}: {e}")
        continue

    # download
    print(f"{counter},{url},{audio_path}")
    audio_data = requests.get(audio_src)
    with open(audio_path, "wb") as af:
        af.write(audio_data.content)

    # convert or copy
    if audio_path.lower().endswith('.mp3') and is_mp3(audio_path):
        print(f"Already MP3; copying to mp3 folder: {audio_path}")
        shutil.copy2(audio_path, mp3_path)
    else:
        print(f"Converting to MP3: {audio_path} -> {mp3_path}")
        if not convert_to_mp3(audio_path, mp3_path):
            print(f"Conversion failed for {audio_path}")

print("Processing complete.")
