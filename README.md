# Karnlada Songs - Music Player Generator

A complete solution to create shareable HTML music players from OneDrive-hosted audio files, deployed to GitHub Pages.

## Features

- Generate beautiful HTML music players with album art
- Auto-play functionality
- Open Graph metadata for rich previews on Messenger and social media
- Responsive design that works on all devices
- GitHub Pages hosting for easy sharing
- Batch processing of multiple songs

## Prerequisites

- Python 3.x installed
- Git installed
- GitHub account
- OneDrive account with public sharing enabled

## Quick Start

### 1. Get Your OneDrive Public Links

For each music file and album art image:

1. Upload files to OneDrive
2. Right-click the file > Share
3. Click "Copy link"
4. Ensure "Anyone with the link can view" is selected
5. For direct streaming, you need the download/embed URL format

**Converting OneDrive Links:**

OneDrive share links look like:
```
https://onedrive.live.com/?id=ABC123...
```

For direct playback, you need download URLs. Options:
- Use OneDrive's "Embed" option to get direct URLs
- Modify the URL to use `/download` endpoint
- Use the link as-is and test if it streams directly

### 2. Configure Your Music Files

Edit `list_onedrive_files.py` and add your songs to the `files` list:

```python
files = [
    {
        "title": "Beautiful Song",
        "artist": "Amazing Artist",
        "audio_url": "https://onedrive.live.com/download?...",
        "album_art_url": "https://onedrive.live.com/download?..."
    },
    {
        "title": "Another Great Track",
        "artist": "Cool Singer",
        "audio_url": "https://onedrive.live.com/download?...",
        "album_art_url": "https://onedrive.live.com/download?..."
    },
]
```

### 3. Run the Complete Workflow

```bash
python run_all.py
```

This will:
1. Process your OneDrive file list
2. Generate HTML music players
3. Optionally deploy to GitHub Pages
4. Show you the public URLs to share

### 4. Enable GitHub Pages

After first push, enable GitHub Pages:

1. Go to: https://github.com/kacharuk/karnlada_songs/settings/pages
2. Under "Source", select **main** branch
3. Select **/docs** folder
4. Click "Save"

Wait a few minutes for deployment, then your site will be live at:
```
https://kacharuk.github.io/karnlada_songs/
```

## Individual Scripts

You can also run scripts separately:

### List OneDrive Files
```bash
python list_onedrive_files.py
```
Creates `onedrive_files.json` with your music file information.

### Generate HTML Players
```bash
python generate_players.py
```
Reads `onedrive_files.json` and creates HTML files in the `docs/` directory.

### Deploy to GitHub
```bash
python deploy.py
```
Commits and pushes HTML files to GitHub.

Optional: Add custom commit message:
```bash
python deploy.py "Added new songs"
```

## File Structure

```
karnlada_songs/
├── list_onedrive_files.py    # Configure your music files here
├── generate_players.py        # Generates HTML players
├── deploy.py                  # Deploys to GitHub
├── run_all.py                 # Runs complete workflow
├── README.md                  # This file
├── onedrive_files.json        # Generated file list
├── generated_urls.json        # Generated public URLs
└── docs/                      # Generated HTML files
    ├── index.html             # Landing page with all songs
    ├── song_title_1.html      # Individual player pages
    └── song_title_2.html
```

## Sharing on Messenger

When you share a link on Messenger, it will automatically display:
- Song title
- Artist name
- Album art image
- Play button

The HTML includes Open Graph meta tags for rich social media previews.

## Troubleshooting

### Audio won't play
- Verify OneDrive link is a direct download URL
- Check browser console for CORS errors
- Some browsers block autoplay - users may need to click play
- Test the OneDrive URL directly in browser

### Album art not showing
- Verify the image URL is accessible
- Check image format (JPEG, PNG work best)
- Ensure OneDrive sharing is set to public

### GitHub Pages not updating
- Wait 5-10 minutes after pushing
- Check GitHub Pages settings are correct
- Verify files are in `/docs` folder
- Check GitHub Actions tab for build status

### Git authentication fails
- Use GitHub CLI: `gh auth login`
- Or create a Personal Access Token
- Or set up SSH keys

### No changes to commit
- Make sure you edited `list_onedrive_files.py`
- Check that `onedrive_files.json` was created
- Verify `docs/` folder contains HTML files

## Updating Songs

To add or update songs:

1. Edit `list_onedrive_files.py`
2. Run `python run_all.py`
3. Confirm deployment when prompted

## Advanced Configuration

### Custom GitHub Pages URL

Edit `base_url` in `generate_players.py`:
```python
base_url = "https://your-username.github.io/your-repo"
```

### Custom Styling

Edit the CSS in `generate_players.py` in the `generate_html_player()` function.

### Different Branch or Folder

To use a different branch or folder for GitHub Pages:
1. Modify the deployment script
2. Update GitHub Pages settings to match

## Requirements

- Python 3.6 or higher
- Git
- Internet connection
- GitHub account with push access to the repository

## Support

For issues or questions:
- Check the Troubleshooting section above
- Review error messages carefully
- Ensure all prerequisites are met
- Verify OneDrive links are publicly accessible

## License

Free to use and modify for personal projects.

---

**Note:** This solution runs locally on your machine. You control all the data and deployment.
