# Quick Start Guide

## Step-by-Step Instructions

### 1. Get OneDrive Links (5 minutes)

For **each song**, you need TWO links:
- Audio file link (MP3 or M4A)
- Album art image link (JPG or PNG)

**How to get OneDrive public links:**

1. Upload your files to OneDrive
2. Right-click the file
3. Click "Share"
4. Select "Anyone with the link can view"
5. Click "Copy link"

**Important:** You may need to convert the link to a direct download URL:
- OneDrive share links: `https://onedrive.live.com/?id=...`
- Direct download links: `https://onedrive.live.com/download?...`

### 2. Add Your Songs (2 minutes)

Open `list_onedrive_files.py` in a text editor and find the `files` list (around line 15).

Add your songs:

```python
files = [
    {
        "title": "My First Song",
        "artist": "The Artist",
        "audio_url": "YOUR_ONEDRIVE_AUDIO_LINK_HERE",
        "album_art_url": "YOUR_ONEDRIVE_IMAGE_LINK_HERE"
    },
    {
        "title": "My Second Song",
        "artist": "Another Artist",
        "audio_url": "YOUR_ONEDRIVE_AUDIO_LINK_HERE",
        "album_art_url": "YOUR_ONEDRIVE_IMAGE_LINK_HERE"
    },
]
```

Save the file.

### 3. Run the Workflow (1 minute)

Open terminal/command prompt in this directory and run:

```bash
python run_all.py
```

Follow the prompts:
- It will process your files
- Generate HTML players
- Ask if you want to deploy to GitHub (say 'y')

### 4. Enable GitHub Pages (1 minute)

**First time only:**

1. Go to: https://github.com/kacharuk/karnlada_songs/settings/pages
2. Under "Source", select: **main** branch
3. Select folder: **/docs**
4. Click "Save"

Wait 2-3 minutes for deployment.

### 5. Get Your Share Links

After GitHub Pages is deployed, your URLs will be:

```
https://kacharuk.github.io/karnlada_songs/song_title.html
```

The script will display all URLs. Copy and share on Messenger!

## Example

Here's a complete example:

**list_onedrive_files.py:**
```python
files = [
    {
        "title": "Summer Breeze",
        "artist": "Karnlada",
        "audio_url": "https://onedrive.live.com/download?cid=ABC123&resid=DEF456&authkey=GHI789",
        "album_art_url": "https://onedrive.live.com/download?cid=ABC123&resid=JKL012&authkey=MNO345"
    },
]
```

**Generated URL:**
```
https://kacharuk.github.io/karnlada_songs/summer_breeze.html
```

Share this URL on Messenger - it will show:
- Title: Summer Breeze
- Artist: Karnlada
- Album art preview
- Play button

## Troubleshooting

**"Audio won't play"**
- Test your OneDrive audio link directly in a browser
- Make sure it's a direct download/stream link
- Check that sharing is set to "Anyone with the link"

**"GitHub Pages not working"**
- Wait 5-10 minutes after first push
- Check GitHub Pages settings (step 4 above)
- Make sure you're using `/docs` folder

**"Git authentication error"**
- Install GitHub CLI: `gh auth login`
- Or use a Personal Access Token

## Adding More Songs

1. Edit `list_onedrive_files.py` (add to the files list)
2. Run `python run_all.py`
3. Confirm deployment

Done! New songs will be added to your site.

## Need Help?

Check the full README.md for detailed information and advanced options.
