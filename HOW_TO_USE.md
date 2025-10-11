# How to Use - Complete Guide

You have 171 songs that need OneDrive share links. Here's the easiest way to set everything up:

## Quick Overview

1. Create OneDrive share links for your songs
2. Collect them using the interactive Python script
3. Generate HTML players
4. Deploy to GitHub Pages
5. Share the URLs!

## Step-by-Step Instructions

### Step 1: Run the Interactive Link Collector

```bash
python collect_links_interactive.py
```

**What this does:**
- Shows you each song title (171 total)
- Asks you to paste the OneDrive share link
- Auto-saves every 10 songs (so you can take breaks!)
- Skips songs you already configured
- Updates the configuration when done

### Step 2: Get OneDrive Share Links

For each song, the script will ask for a link. Here's how to get it:

**Method A - File Explorer (Fastest):**
1. Open: `C:\Users\kacha\OneDrive\_Old_Backup\Karnlada Songs`
2. Navigate to the subfolder (e.g., "Karnlada Music")
3. Right-click the audio file
4. Click "Share" (OneDrive option)
5. Click "Copy link"
6. Paste into the Python script

**Method B - OneDrive Web:**
1. Go to onedrive.live.com
2. Navigate to your music folder
3. Right-click file → Share → Copy link

### Step 3: Tips for Efficiency

**You can do this in batches:**
- Collect links for 20-30 songs at a time
- The script auto-saves every 10 songs
- Press Enter to skip songs
- Type 'quit' to save and exit
- Run the script again to continue where you left off

**Recommended approach:**
1. Open File Explorer to your music folder
2. Open the Python script in terminal
3. For each song:
   - Find it in File Explorer
   - Right-click → Share → Copy link
   - Paste into terminal
   - Repeat

### Step 4: Generate HTML Players

Once you've collected all (or some) links:

```bash
python run_all.py
```

This will:
1. Read your collected links
2. Generate beautiful HTML music players
3. Ask if you want to deploy to GitHub
4. Show you the public URLs

### Step 5: Deploy and Share

After generation:
1. Answer 'y' when asked to deploy
2. Wait for GitHub Pages to update (2-3 minutes)
3. Share the URLs on Messenger!

## Your Configuration

All songs will have:
- **Artist:** กาญจน์ลดา มฤคพิทักษ์ (hardcoded)
- **Album Art:** https://1drv.ms/i/c/19724284c9b34401/EaRNlSs0VH9IpgzboKat2vYBNdVlQ9a4WWOoIvvnracDrA?e=s9mA4Q (hardcoded)
- **Title:** Extracted from filename
- **Audio URL:** The OneDrive link you provide

## File Organization

Your 171 songs are in these folders:
```
Karnlada Songs/
├── Karnlada Music/ (43 files)
├── Karnlada Music 2/ (46 files)
├── กาญจน์ลดา มฤคพิทักษ์ - กาญจน์ลดา 1/ (17 files)
├── กาญจน์ลดา มฤคพิทักษ์ - กาญจน์ลดา 2/ (16 files)
├── กาญจน์ลดา มฤคพิทักษ์ - กาญจน์ลดา 3/ (17 files)
├── ชรินทร์ ชุดที่ 1/ (17 files)
└── ชรินทร์ ชุดที่ 2/ (15 files)
```

## Progress Tracking

The script tracks your progress in `songs_config.json`:
- Shows which songs are already configured
- Skips them automatically on next run
- You can see how many remain

## Troubleshooting

**Script says "already configured":**
- This is good! It means you already added this song
- The script skips it automatically

**Want to start over:**
- Delete `songs_config.json`
- Run the script again

**Want to update a specific song:**
- Edit `songs_config.json` manually
- Or delete that entry and run the script again

**Audio won't play in browser:**
- Make sure the OneDrive link is set to "Anyone with the link can view"
- Try the embed URL format instead
- Test the link directly in your browser

## Expected Timeline

If you do 20 songs per session:
- Session 1: Songs 1-20 (20 minutes)
- Session 2: Songs 21-40 (20 minutes)
- ... and so on
- Total: About 9 sessions = 3 hours spread over a few days

You can deploy after each session to test!

## Commands Summary

```bash
# Collect OneDrive links interactively
python collect_links_interactive.py

# Generate HTML and deploy (after collecting links)
python run_all.py

# Or run steps separately:
python list_onedrive_files.py    # Process configuration
python generate_players.py        # Generate HTML
python deploy.py                  # Deploy to GitHub
```

## What You'll Get

After deployment, each song will have a URL like:
```
https://kacharuk.github.io/karnlada_songs/song_title.html
```

When shared on Messenger, it shows:
- Song title
- Artist name (กาญจน์ลดา มฤคพิทักษ์)
- Album art preview
- Play button

## Next Steps

1. **Start collecting links:** `python collect_links_interactive.py`
2. **Take your time:** You can do this in multiple sessions
3. **Test as you go:** Deploy after collecting 20-30 songs to test
4. **Share your favorites:** Start sharing URLs on Messenger!

---

**Ready?** Run `python collect_links_interactive.py` to begin!
