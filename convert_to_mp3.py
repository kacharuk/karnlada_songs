#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

# Define ffmpeg paths
FFMPEG_PATH = r"C:\tools\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\tools\ffmpeg\bin\ffprobe.exe"

def is_mp3(file_path):
    """Check if file is actually an MP3 using ffprobe"""
    try:
        result = subprocess.run([
            FFPROBE_PATH,  # Use absolute path
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
    """Convert audio file to MP3 using ffmpeg"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        subprocess.run([
            FFMPEG_PATH,  # Use absolute path
            '-i', input_path,
            '-codec:a', 'libmp3lame',
            '-b:a', bitrate,
            '-map_metadata', '0',
            '-y',  # Overwrite output file if exists
            output_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e}")
        return False

def process_audio_files():
    """Process all audio files under docs/audio"""
    source_dir = Path('./m4a')
    target_dir = Path('./m4a/mp3')
    
    # Create output directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Audio file extensions to process
    audio_extensions = {'.mp3', '.m4a', '.wav', '.aac', '.ogg', '.flac'}
    
    # Track statistics
    stats = {'converted': 0, 'copied': 0, 'skipped': 0, 'failed': 0}
    
    for audio_file in source_dir.rglob('*'):
        # Skip the mp3 output directory itself
        if 'mp3' in audio_file.parts:
            continue
            
        if audio_file.suffix.lower() in audio_extensions:
            # Calculate relative path to maintain directory structure
            rel_path = audio_file.relative_to(source_dir)
            output_path = target_dir / rel_path
            output_path = output_path.with_suffix('.mp3')
            
            print(f"Processing: {rel_path}")
            
            # Check if it's already an MP3
            if audio_file.suffix.lower() == '.mp3' and is_mp3(audio_file):
                print(f"Copying (already MP3): {rel_path}")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                shutil.copy2(audio_file, output_path)
                stats['copied'] += 1
            else:
                print(f"Converting to MP3: {rel_path}")
                if convert_to_mp3(str(audio_file), str(output_path)):
                    stats['converted'] += 1
                else:
                    stats['failed'] += 1
                    continue
    
    # Print summary
    print("\nConversion Summary:")
    print(f"Converted: {stats['converted']}")
    print(f"Copied (already MP3): {stats['copied']}")
    print(f"Failed: {stats['failed']}")
    print(f"\nOutput directory: {target_dir}")

if __name__ == '__main__':
    print("Audio File Converter")
    print("==================")
    
    # Check for ffmpeg tools
    if not os.path.exists(FFMPEG_PATH):
        print(f"Error: ffmpeg not found at {FFMPEG_PATH}")
        exit(1)
    if not os.path.exists(FFPROBE_PATH):
        print(f"Error: ffprobe not found at {FFPROBE_PATH}")
        exit(1)
        
    process_audio_files()
