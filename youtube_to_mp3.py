#!/usr/bin/env python3
"""
Simple YouTube -> MP3 batch downloader.

Reads URLs (one per line) from `youtube_list.txt` by default and
downloads each video's audio as an MP3 into the `mp3/` folder.

Usage:
    python youtube_to_mp3.py [input_file] [output_dir]

Requirements:
    - ffmpeg installed and on PATH
    - Python package: yt-dlp (see requirements.txt)

Lines beginning with `#` or empty lines are ignored.
"""
import os
import sys
import shutil
from yt_dlp import YoutubeDL


def read_urls(path):
    with open(path, encoding='utf-8') as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            yield line


def make_ydl_opts(outdir, ffmpeg_location=None):
    opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(outdir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'continuedl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True,
        'ignoreerrors': True,
    }
    if ffmpeg_location:
        # yt-dlp accepts 'ffmpeg_location' to point to ffmpeg binary directory
        opts['ffmpeg_location'] = ffmpeg_location
    return opts


def download_audio(url, outdir, ffmpeg_location=None):
    opts = make_ydl_opts(outdir, ffmpeg_location)
    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def main():
    infile = sys.argv[1] if len(sys.argv) > 1 else 'youtube_list.txt'
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join('output', 'yt')

    # Ensure ffmpeg is available for audio extraction/conversion
    ffmpeg_location = None
    if shutil.which('ffmpeg'):
        # ffmpeg on PATH -> no extra config needed
        ffmpeg_location = None
    else:
        # Check environment variable first
        env_path = os.environ.get('FFMPEG_PATH') or os.environ.get('FFMPEG_BINARY')
        if env_path:
            # if user provided full path to exe, use its directory
            if os.path.isfile(env_path):
                ffmpeg_location = os.path.dirname(os.path.abspath(env_path))
            elif os.path.isdir(env_path):
                ffmpeg_location = os.path.abspath(env_path)
        # common local install used by user
        if ffmpeg_location is None:
            common = os.path.join('C:', os.sep, 'tools', 'ffmpeg', 'bin', 'ffmpeg.exe')
            if os.path.isfile(common):
                ffmpeg_location = os.path.dirname(common)

        if ffmpeg_location is None:
            print('ffmpeg not found on PATH. Install ffmpeg and ensure it is available on your PATH,', file=sys.stderr)
            print('or set the FFMPEG_PATH environment variable to the ffmpeg binary or folder.', file=sys.stderr)
            print('On Windows you can use Chocolatey: `choco install ffmpeg` or download from ffmpeg.org', file=sys.stderr)
            sys.exit(3)

    if not os.path.exists(infile):
        print(f'Input file not found: {infile}', file=sys.stderr)
        sys.exit(2)

    os.makedirs(outdir, exist_ok=True)

    for url in read_urls(infile):
        try:
            print(f'Downloading: {url}')
            download_audio(url, outdir, ffmpeg_location)
        except Exception as exc:
            print(f'Failed: {url} -> {exc}', file=sys.stderr)


if __name__ == '__main__':
    main()
