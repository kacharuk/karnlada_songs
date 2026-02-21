import os
import sys
# sys.path.append("path_to_your_python_site_packages")  # Replace with the actual path to site-packages
import requests
from bs4 import BeautifulSoup
import subprocess
import json
import re


def unique_filename(base, ext):
    """Return a filename that doesn't conflict by appending a suffix.

    base: filename without extension
    ext: extension including the leading dot (e.g. ".mp4")
    """
    candidate = f"{base}{ext}"
    counter = 2
    while os.path.exists(candidate):
        candidate = f"{base}-{counter}{ext}"
        counter += 1
    return candidate


counter = 0

# ensure output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1: Read URLs from list.txt
with open("list.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

# Step 2: Loop through URLs and process each
for url in urls:
    counter += 1
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the <script> tag containing the JSON data
    script_tag = soup.find("script", text=lambda t: t and "window.__DATA__" in t)
    if not script_tag:
        print(f"No script tag with audio data found in {url}")
        continue

    # Extract and parse the JSON data
    try:
        # Use a regular expression to extract the JSON object
        match = re.search(r"window\.__DATA__\s*=\s*(\{.*?\});", script_tag.string, re.DOTALL)
        if not match:
            raise ValueError("JSON data not found in script tag")
        
        json_text = match.group(1)  # Extract the JSON object
        data = json.loads(json_text)  # Parse the JSON string
        audio_src = data["detail"].get("playurl")
        if not audio_src:
            print(f"No audio source found for {url}")
            raise ValueError("playurl missing")

        audio_title = data["detail"]["song_name"].replace("/", "-")
        
        # generate non-conflicting filenames for audio/video inside output folder
        audio_filename = unique_filename(os.path.join(OUTPUT_DIR, audio_title), ".m4a")
        video_filename = unique_filename(os.path.join(OUTPUT_DIR, audio_title), ".mp4")
        
    except (KeyError, IndexError, json.JSONDecodeError, ValueError) as e:
        print(f"Failed to extract audio data from {url}: {e}")
        continue

    # Step 3: Download the .m4a file
    # audio_filename already determined above via unique_filename
    print(f"{counter},{url},{audio_filename}")  # file written under {OUTPUT_DIR}
    audio_data = requests.get(audio_src)
    with open(audio_filename, "wb") as audio_file:
        audio_file.write(audio_data.content)

    # Step 4: Create an .mp4 video using photo.jpg
    # if not os.path.exists("photo.jpg"):
    #     print("photo.jpg not found in the root folder. Skipping video creation.")
    #     continue

    # video_filename = f"{audio_title}.mp4"
    # print(f"Creating video {video_filename} using ffmpeg...")
    # try:
    #     subprocess.run([
    #         "C:\\tools\\ffmpeg\\bin\\ffmpeg.exe", "-loop", "1", "-i", "photo.jpg", "-i", audio_filename,
    #         "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
    #         "-pix_fmt", "yuv420p", "-shortest", video_filename
    #     ], check=True)
    # except subprocess.CalledProcessError as e:
    #     print(f"Error creating video {video_filename}: {e}")
    #     continue

    # Cleanup
    # os.remove(audio_filename)

print("Processing complete.")
