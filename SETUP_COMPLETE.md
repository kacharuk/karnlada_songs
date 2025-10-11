# Setup Complete!

Your Karnlada Songs music player generator is ready to use.

## What You Have

A complete local solution with 4 Python scripts:

1. **list_onedrive_files.py** - Configure your music files here
2. **generate_players.py** - Generates HTML music players
3. **deploy.py** - Deploys to GitHub Pages
4. **run_all.py** - Runs the complete workflow

## What It Does

1. Takes your OneDrive-hosted music files (MP3/M4A)
2. Generates beautiful HTML music players with album art
3. Pushes them to GitHub Pages
4. Gives you shareable URLs that work great on Messenger

## Next Steps

### Step 1: Add Your Music Files

Edit `list_onedrive_files.py` and add your songs:

```python
files = [
    {
        "title": "Song Title",
        "artist": "Artist Name",
        "audio_url": "https://onedrive.live.com/download?...",
        "album_art_url": "https://onedrive.live.com/download?..."
    },
]
```

### Step 2: Run the Workflow

```bash
python run_all.py
```

### Step 3: Enable GitHub Pages (First Time Only)

1. Go to: https://github.com/kacharuk/karnlada_songs/settings/pages
2. Source: **main** branch
3. Folder: **/docs**
4. Click Save

### Step 4: Share Your Music!

Your URLs will be:
```
https://kacharuk.github.io/karnlada_songs/song_name.html
```

## Features

- **Auto-play** - Music starts automatically
- **Album Art** - Beautiful cover images
- **Messenger Preview** - Rich previews when shared
- **Responsive** - Works on all devices
- **Easy Updates** - Just edit and run again

## File Overview

```
karnlada_songs/
├── list_onedrive_files.py    ← EDIT THIS to add songs
├── generate_players.py
├── deploy.py
├── run_all.py                 ← RUN THIS for complete workflow
├── README.md                  ← Full documentation
├── QUICKSTART.md             ← Step-by-step guide
└── docs/                      ← Generated HTML files (created after first run)
```

## Important Notes

- **OneDrive Links**: Make sure they're direct download/streaming URLs
- **Public Sharing**: Must be set to "Anyone with the link can view"
- **GitHub Pages**: Takes 2-3 minutes to update after pushing
- **First Time**: You'll need to authenticate with GitHub

## Getting OneDrive Links

1. Upload file to OneDrive
2. Right-click > Share
3. "Anyone with the link can view"
4. Copy link
5. You may need to convert to direct download URL

## Troubleshooting

**Can't play audio?**
- Test OneDrive link directly in browser
- Ensure it's a direct streaming URL

**GitHub push fails?**
- Run: `gh auth login`
- Or set up SSH keys

**Pages not updating?**
- Wait 5-10 minutes
- Check GitHub Pages settings
- Look at Actions tab for errors

## Need Help?

- Read QUICKSTART.md for detailed step-by-step
- Read README.md for full documentation
- Check error messages carefully

## Example Workflow

```bash
# 1. Edit your songs
notepad list_onedrive_files.py

# 2. Run complete workflow
python run_all.py

# 3. Answer 'y' when asked to deploy

# 4. Wait 3 minutes for GitHub Pages

# 5. Share your URLs on Messenger!
```

## What Happens When You Share on Messenger?

When someone receives your link, they'll see:
- Song title
- Artist name
- Album art preview
- "Play" button

Click the link to open the music player:
- Full album art display
- Audio controls
- Auto-play (if browser allows)
- Beautiful, responsive design

---

**Ready to get started? Edit `list_onedrive_files.py` and add your first song!**
