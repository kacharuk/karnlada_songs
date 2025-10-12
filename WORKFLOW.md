# Karnlada Songs - Maintenance Workflow

This document describes the complete workflow for maintaining the Karnlada Songs music library.

## Overview

The system consists of:
- **Python scripts**: For scanning files and generating HTML
- **CSV file** (`songs_mapping.csv`): Master database of all songs
- **HTML files**: Generated pages for index, player, and individual songs
- **JavaScript modules**: Reusable utilities for search, sharing, QR codes, and player

## Your Maintenance Workflow

### Step 1: Add New Songs

1. Copy new audio files (mp3/m4a) to `docs/audio/{album}/`
   - Organize by album folders
   - Include album art as `album_art.jpg` in each album folder
   - Files should be named: `NN. Title - Artist.mp3` (number prefix optional)

### Step 2: Scan for New Songs

Run the scan script to update the CSV:

```bash
python scan_new_songs.py
```

This script will:
- Scan all files in `docs/audio/`
- Generate stable IDs for new songs
- Add new entries to `songs_mapping.csv`
- Preserve existing songs (no duplicates)
- Extract titles from filenames (removes number prefixes)
- Set default artist to "กาญจน์ลดา มฤคพิทักษ์"

### Step 3: Review and Edit CSV

Open `songs_mapping.csv` in a text editor or spreadsheet program.

You can:
- **Reorder songs**: Cut and paste rows to change order
- **Fix titles**: Edit the `title` column
- **Change artist**: Edit the `artist` column (rare)
- **Add external links**:
  - Add a row with `is_external=true`
  - Set `audio_file_path` to the full external URL (YouTube, SoundCloud, etc.)
  - Choose a unique `song_id` (8 characters, letters/numbers)
  - Example:
    ```csv
    youtube01,YouTube,Song Title,กาญจน์ลดา มฤคพิทักษ์,https://youtube.com/watch?v=xxx,youtube01.html,true
    ```

**CSV Format:**
```csv
song_id,album,title,artist,audio_file_path,html_filename,is_external
abc12345,Album Name,Song Title,กาญจน์ลดา มฤคพิทักษ์,audio/Album Name/file.mp3,abc12345.html,false
```

### Step 4: Generate HTML Files

Run the rebuild script to generate all HTML:

```bash
python rebuild.py
```

This will:
1. Run `scan_new_songs.py` (updates CSV if needed)
2. Run `generate_html.py` (generates all HTML files)

Generated files:
- `docs/index.html` - Enhanced index with search, share buttons, QR codes, playlist buttons
- `docs/player.html` - Enhanced player with playlist support
- `docs/songs/*.html` - Individual stub pages for each song (with Open Graph metadata)
- `docs/js/utils.js` - Utility functions (sharing, QR codes, time formatting)
- `docs/js/search.js` - Search functionality for index page
- `docs/js/player.js` - Player logic with playlist support

### Step 5: Test Locally (Optional)

Open `docs/index.html` in your browser to test:
- Search functionality
- Share buttons
- QR code generation
- Playlist buttons
- Individual song pages

### Step 6: Deploy to GitHub

```bash
git add -A
git commit -m "Add new songs from [Album Name]"
git push
```

GitHub Pages will automatically deploy your changes to:
https://kacharuk.github.io/karnlada_songs/

## Features

### Index Page Features
- ✅ **Search bar**: Live search through all songs
- ✅ **Album organization**: Songs grouped by album
- ✅ **Share buttons**: Share individual songs via Web Share API or clipboard
- ✅ **QR code buttons**: Generate QR codes for easy mobile sharing
- ✅ **Playlist buttons**: Play entire albums as playlists

### Player Features
- ✅ **Single song mode**: `player.html?id=song123`
- ✅ **Playlist mode**: `player.html?ids=song1,song2,song3`
- ✅ **Auto-advance**: Automatically plays next song in playlist
- ✅ **Skip external links**: Skips songs with external URLs
- ✅ **Preloading**: Preloads next song in last 15 seconds
- ✅ **Playlist UI**: Shows all songs with currently playing indicator
- ✅ **Next song info**: Displays upcoming song title

### Technical Features
- ✅ **Stable IDs**: Song URLs never change even if files are renamed
- ✅ **Modular JavaScript**: Reusable utilities in separate files
- ✅ **Open Graph metadata**: Proper previews when sharing on social media
- ✅ **External link support**: Can link to YouTube, SoundCloud, etc.
- ✅ **Mobile responsive**: Works great on phones and tablets
- ✅ **No dependencies**: Uses only vanilla JavaScript and free APIs

## File Structure

```
karnlada_songs/
├── docs/                          # GitHub Pages root
│   ├── index.html                 # Main page (generated)
│   ├── player.html                # Music player (generated)
│   ├── songs/                     # Individual song pages
│   │   ├── abc12345.html
│   │   └── ...
│   ├── audio/                     # Audio files (you manage)
│   │   ├── Album 1/
│   │   │   ├── album_art.jpg
│   │   │   ├── 01. Song.mp3
│   │   │   └── ...
│   │   └── Album 2/
│   │       └── ...
│   ├── images/                    # Images
│   │   └── album_art_karnlada.jpg # Default album art
│   └── js/                        # JavaScript modules
│       ├── utils.js               # Utilities (sharing, QR, etc.)
│       ├── search.js              # Search functionality
│       └── player.js              # Player with playlist support
├── songs_mapping.csv              # Master song database (YOU EDIT THIS)
├── onedrive_files.json            # Generated metadata
├── scan_new_songs.py              # Scan for new files
├── generate_html.py               # Generate all HTML
├── rebuild.py                     # Complete rebuild
└── WORKFLOW.md                    # This file
```

## Troubleshooting

**Q: New songs don't appear**
- Make sure you ran `python scan_new_songs.py`
- Check that `songs_mapping.csv` has the new entries
- Run `python rebuild.py` to regenerate HTML

**Q: Song title is wrong**
- Edit the `title` column in `songs_mapping.csv`
- Run `python rebuild.py`

**Q: Want to add external link (YouTube)**
- Add a row to `songs_mapping.csv` with `is_external=true`
- Set `audio_file_path` to the full YouTube URL
- Run `python rebuild.py`

**Q: Playlist button doesn't work**
- Make sure all songs in the album have valid `song_id` values
- Check browser console for errors

**Q: QR code doesn't show**
- QR codes use https://api.qrserver.com/ (free service)
- Check internet connection
- Try a different browser

**Q: Search doesn't find songs**
- Make sure JavaScript files are loaded (check docs/js/)
- Search is case-insensitive and searches song titles only

## Advanced: External Links

To add songs from YouTube, SoundCloud, or other platforms:

1. Edit `songs_mapping.csv`
2. Add a row with these values:
   - `song_id`: Unique 8-character ID (e.g., `youtube01`)
   - `album`: Album name (can be "YouTube" or "External")
   - `title`: Song title in Thai
   - `artist`: กาญจน์ลดา มฤคพิทักษ์
   - `audio_file_path`: **Full external URL** (e.g., `https://youtube.com/watch?v=xxx`)
   - `html_filename`: Same as song_id with `.html` (e.g., `youtube01.html`)
   - `is_external`: **true**

3. Run `python rebuild.py`

External links will:
- Appear in the index
- Show in playlists with "[external link]" label
- Be skipped during playlist playback
- Redirect users directly to the external platform

## Backup

Your most important file is `songs_mapping.csv`. Always back it up before making major changes.

The CSV is your source of truth. HTML files can always be regenerated from it.

## Need Help?

Check these files for more details:
- `EXTERNAL_LINKS.md` - How to add external links
- `scan_new_songs.py` - How the scanner works
- `generate_html.py` - How HTML is generated
- `docs/js/*.js` - JavaScript functionality
