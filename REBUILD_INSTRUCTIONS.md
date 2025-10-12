# How to Update Songs

This document explains how to add, edit, or remove songs from your music library.

## Quick Rebuild Process

Whenever you make changes to audio files, simply run:

```bash
python rebuild.py
```

This will automatically:
1. ✅ Scan all MP3/M4A files in `docs/audio/` and subfolders
2. ✅ Extract song titles (removing number prefixes like "01.", "02 ")
3. ✅ Generate stub pages for each song with social media metadata
4. ✅ Generate central player (`player.html`)
5. ✅ Generate album-organized index page (`index.html`)

Then deploy to GitHub:
```bash
git add -A
git commit -m "Update songs"
git push
```

## Adding New Songs

### Option 1: Add to Existing Album
1. Copy your MP3/M4A files into the appropriate album folder
   - Example: `docs/audio/Karnlada Music/new-song.mp3`
2. Run `python rebuild.py`
3. Deploy changes

### Option 2: Create New Album
1. Create a new folder under `docs/audio/`
   - Example: `docs/audio/New Album Name/`
2. Copy your MP3/M4A files into it
3. (Optional) Add `album_art.jpg` for custom album art
4. Run `python rebuild.py`
5. Deploy changes

## File Naming Convention

### Song Files
Format: `[number] Song Title - Artist Name.ext`

Examples:
- `01. กล้วยไม้ - กาญจน์ลดา มฤคพิทักษ์.mp3` → Title: "กล้วยไม้"
- `02 ถึงเธอ.mp3` → Title: "ถึงเธอ"
- `ดอกไม้กับเพลง.m4a` → Title: "ดอกไม้กับเพลง"

**Note:** Numbers are automatically removed from titles in the display.

### Album Art
- Place `album_art.jpg` in each album folder for custom art
- Falls back to `docs/images/album_art_karnlada.jpg` if not found

## Project Structure

```
docs/
├── audio/                          # All audio files organized by albums
│   ├── Karnlada Music/
│   │   ├── album_art.jpg          # Album-specific cover art
│   │   ├── song1.mp3
│   │   └── song2.mp3
│   ├── Karnlada Music 2/
│   │   ├── album_art.jpg
│   │   └── ...
│   └── [More Album Folders]/
│
├── images/
│   └── album_art_karnlada.jpg     # Default album art
│
├── index.html                      # Main page (album browser)
├── player.html                     # Central music player
├── [song-name].html                # Stub pages (171+)
│
├── onedrive_files.json             # Song metadata
└── generated_urls.json             # URL list

Root files:
├── rebuild.py                      # ⭐ Main rebuild script
├── list_onedrive_files.py         # Scans audio files
├── generate_players.py             # Generates HTML pages
└── REBUILD_INSTRUCTIONS.md         # This file
```

## Customization

### Change Album Order
Songs are displayed alphabetically within albums. To reorder:
- Rename files with number prefixes (e.g., `01`, `02`, `03`)
- Numbers are stripped from display automatically

### Custom Album Art
- Add `album_art.jpg` to any album folder
- Recommended size: 1000x1000px or larger
- Format: JPG

### Edit Song Metadata
The scanner extracts:
- **Title**: From filename (after removing numbers, before " - ")
- **Artist**: From filename (after " - "), defaults to "กาญจน์ลดา มฤคพิทักษ์"
- **Album**: From folder name

## URLs

After deployment, songs are available at:
- Index: `https://kacharuk.github.io/karnlada_songs/`
- Player: `https://kacharuk.github.io/karnlada_songs/player.html?id=song.html`
- Songs: `https://kacharuk.github.io/karnlada_songs/[song-name].html`

## Troubleshooting

### Songs not showing up?
Run `python rebuild.py` and check for errors.

### Wrong song titles?
Check filename format: `[number]. Title - Artist.mp3`

### Album art not displaying?
- Ensure file is named `album_art.jpg` (lowercase)
- Place in the album folder
- Run `python rebuild.py`

---

**That's it!** Just run `rebuild.py` whenever you modify audio files.
