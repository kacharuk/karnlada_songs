# Karnlada Songs - Music Library

A simple music library website with search, sharing, QR codes, and playlist support. All songs are organized by album with local audio files.

## ✨ Features

- 🔍 **Live search** - Find songs instantly as you type
- 📤 **Share buttons** - Share songs via Web Share API or clipboard
- 🔳 **QR codes** - Generate QR codes for easy mobile sharing
- ▶️ **Playlist mode** - Play entire albums with auto-advance
- 🎵 **Smart player** - Preloads next song, skips external links
- 📱 **Mobile-friendly** - Responsive design works on all devices
- 🔗 **External links** - Support for YouTube, SoundCloud, etc.
- 🎯 **Stable URLs** - Song links never change even if files are renamed

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- Git
- Audio files (mp3/m4a)

### Initial Setup

1. Clone this repository
2. Copy audio files to `docs/audio/{album}/`
3. Run: `python rebuild.py`
4. Push to GitHub
5. Enable GitHub Pages (Settings → Pages → main branch → /docs folder)

Your site will be live at: `https://kacharuk.github.io/karnlada_songs/`

---

## 📝 How to Add/Remove Songs

### Adding New Audio Files

1. **Copy files** to `docs/audio/{album}/`
   ```bash
   # Example:
   cp "new_song.mp3" "docs/audio/Karnlada Music/"
   ```

2. **Add album art** (optional)
   - Place `album_art.jpg` in the album folder
   - If not present, uses default album art

3. **Run rebuild**
   ```bash
   python rebuild.py
   ```
   This will:
   - Scan for new files
   - Generate stable IDs automatically
   - Update `songs_mapping.csv`
   - Create HTML pages

4. **Review** `songs_mapping.csv` (optional)
   - Reorder rows to change song order
   - Edit titles if needed
   - Run `python rebuild.py` again if you made changes

5. **Deploy**
   ```bash
   git add -A
   git commit -m "Add new songs"
   git push
   ```

### Adding External Links (YouTube, SoundCloud, etc.)

1. **Edit** `songs_mapping.csv` manually
2. **Add a new row** with these values:
   ```csv
   song_id,album,title,artist,audio_file_path,html_filename,is_external
   youtube01,YouTube,Song Title,Artist Name,https://youtube.com/watch?v=xxx,youtube01.html,true
   ```
   - `song_id`: Unique 8-char ID (your choice, e.g., `youtube01`)
   - `album`: Album name (e.g., "YouTube" or "External")
   - `title`: Song title
   - `artist`: Artist name
   - `audio_file_path`: **Full external URL**
   - `html_filename`: `{song_id}.html`
   - `is_external`: **true**

3. **Run rebuild**
   ```bash
   python rebuild.py
   ```

4. **Deploy**
   ```bash
   git add -A
   git commit -m "Add external link: Song Title"
   git push
   ```

### Removing Songs

#### Remove Audio File:
1. Delete the audio file from `docs/audio/{album}/`
2. Delete the corresponding row from `songs_mapping.csv`
3. Run `python rebuild.py`
4. Deploy changes

#### Remove External Link:
1. Delete the row from `songs_mapping.csv`
2. Run `python rebuild.py`
3. Deploy changes

### Reordering Songs

Songs appear in the **same order as in the CSV file**.

To change the order:
1. Open `songs_mapping.csv`
2. Cut and paste rows to reorder
3. Save the file
4. Run `python rebuild.py`
5. Deploy changes

---

## 📂 File Structure

```
karnlada_songs/
├── songs_mapping.csv          # Master database (EDIT THIS!)
├── scan_new_songs.py          # Scans for new audio files
├── generate_html.py           # Generates HTML from CSV
├── rebuild.py                 # Main workflow script
├── WORKFLOW.md                # Detailed workflow guide
├── FEATURES.md                # Complete feature list
└── docs/                      # GitHub Pages root
    ├── index.html             # Main page (generated)
    ├── player.html            # Music player (generated)
    ├── songs/                 # Individual song pages (generated)
    │   └── *.html
    ├── audio/                 # Your audio files
    │   ├── Album 1/
    │   │   ├── album_art.jpg
    │   │   └── *.mp3
    │   └── Album 2/
    │       └── *.m4a
    └── js/                    # JavaScript modules (generated)
        ├── utils.js
        ├── search.js
        └── player.js
```

## 🛠️ Commands

### Main Command (Use This!)
```bash
python rebuild.py
```
Scans for new files, updates CSV, generates all HTML.

### Individual Steps
```bash
# Step 1: Scan for new files
python scan_new_songs.py

# Step 2: Generate HTML
python generate_html.py
```

### Deploy to GitHub
```bash
git add -A
git commit -m "Your message here"
git push
```

## 🎯 Common Tasks

### Change Song Order in Album
1. Open `songs_mapping.csv`
2. Reorder rows (cut/paste)
3. `python rebuild.py`
4. Deploy

### Fix Song Title
1. Edit `title` column in `songs_mapping.csv`
2. `python rebuild.py`
3. Deploy

### Change Artist Name
1. Edit `artist` column in `songs_mapping.csv`
2. `python rebuild.py`
3. Deploy

### Add Album Art
1. Place `album_art.jpg` in `docs/audio/{album}/`
2. `python rebuild.py` (detects it automatically)
3. Deploy

## 🔧 Troubleshooting

### New songs not appearing?
- Make sure files are in `docs/audio/{album}/`
- Run `python rebuild.py`
- Check that `songs_mapping.csv` has the new entries

### External link not working?
- Verify `is_external` is set to `true` (lowercase)
- Check the URL is correct
- Run `python rebuild.py` after editing CSV

### Song order is wrong?
- Check the order in `songs_mapping.csv`
- Songs appear in CSV order (not alphabetical)
- Run `python rebuild.py` after reordering

### Changes not showing on website?
- Wait 2-3 minutes after `git push`
- Clear browser cache
- Check GitHub Actions for deployment status

## 📚 Additional Documentation

- **WORKFLOW.md** - Complete maintenance workflow
- **FEATURES.md** - All features and technical details
- **EXTERNAL_LINKS.md** - How to add external links

## 🎵 Song ID System

Each song gets a **stable 8-character ID** based on:
- Album name
- Song title
- File path

**Benefits:**
- URLs never change
- Safe to share and bookmark
- Files can be renamed without breaking links

**Example:**
- File: `docs/audio/Album/Song.mp3`
- ID: `abc12345`
- URL: `https://kacharuk.github.io/karnlada_songs/songs/abc12345.html`

---

## 📄 License

Free to use and modify for personal projects.

**Built for:** กาญจน์ลดา มฤคพิทักษ์'s music collection 🎵
