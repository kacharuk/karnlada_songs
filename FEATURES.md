# Karnlada Songs - Feature Summary

## ✅ All Features Implemented

### Index Page (docs/index.html)

**Search Functionality:**
- Real-time search bar at the top
- Live filtering as you type
- Case-insensitive Thai and English search
- Shows/hides albums based on matches
- "No results" message when nothing found
- Clear button to reset search
- Press Enter to play first result

**Album Organization:**
- Songs grouped by album
- Album index at top for quick navigation
- Song count displayed for each album
- Click album link to scroll to that section

**Per-Song Actions:**
- **Play Button**: Opens song in player
- **Share Button**:
  - Uses Web Share API on mobile (native sharing)
  - Falls back to clipboard copy on desktop
  - Shows confirmation message
- **QR Button**:
  - Generates QR code using free API (qrserver.com)
  - Modal popup with song title and QR image
  - Click outside or X button to close
  - QR code links to full song page (with Open Graph)

**Playlist Feature:**
- Each album has "▶ Play Playlist" button
- Opens player with all songs from that album
- Shows song count in button label

**Responsive Design:**
- Mobile-friendly layout
- Touch-friendly buttons
- Stacks vertically on small screens

### Player Page (docs/player.html)

**Single Song Mode:**
- URL: `player.html?id=song123`
- Plays one song
- Shows song title, artist, album art
- Custom play/pause controls
- Time slider with current/total time
- Share button

**Playlist Mode:**
- URL: `player.html?ids=song1,song2,song3`
- Plays multiple songs in sequence
- Auto-advances to next song
- Skips external links automatically
- Shows "Next: [song name]" info

**Playlist UI:**
- List of all songs at bottom
- Currently playing song highlighted in green
- Click any song to jump to it
- Song numbers/play indicators
- External songs marked as "[external link]"
- Scrollable if many songs

**Smart Loading:**
- Only loads current song initially
- Preloads next song in last 15 seconds
- Saves bandwidth
- Smooth transitions between songs

**Player Controls:**
- Large play/pause button on album art
- Smaller play/pause button below
- Click album art to play/pause
- Time slider for scrubbing
- Share button (copies current URL)

### Individual Song Pages (docs/songs/*.html)

**Open Graph Metadata:**
- Proper previews when shared on:
  - Facebook
  - Twitter/X
  - WhatsApp
  - Messenger
  - LinkedIn
  - etc.
- Includes song title, artist, album art, audio URL

**Instant Redirect:**
- Meta refresh to player in 0 seconds
- Fallback link if redirect fails
- SEO-friendly canonical URL

**External Link Support:**
- Songs with `is_external=true` redirect to external platform
- YouTube, SoundCloud, Spotify, etc.
- Still has Open Graph metadata for sharing

### Backend/Maintenance

**scan_new_songs.py:**
- Scans docs/audio/ for new files
- Generates stable 8-character IDs (MD5 hash)
- Updates songs_mapping.csv with new songs only
- Preserves existing songs (no duplicates)
- Extracts title from filename (removes number prefix)
- Auto-detects album art (album_art.jpg in folder)

**generate_html.py:**
- Generates all HTML files from CSV
- Creates index.html with search/share/QR
- Creates player.html with playlist support
- Creates individual song stub pages
- Copies onedrive_files.json to docs/
- Modular - doesn't regenerate unchanged files

**rebuild.py:**
- Runs scan_new_songs.py first
- Then runs generate_html.py
- One-command complete rebuild
- Shows progress and summary

**Modular JavaScript:**
- **utils.js**: Reusable functions
  - generateQRCodeUrl()
  - showQRCodeModal()
  - shareSong()
  - escapeHtml()
  - getBaseUrl(), getSongShareUrl(), getPlaylistUrl()
  - formatTime()
- **search.js**: Search functionality
  - initializeSearch()
  - performSearch()
  - clearSearch()
- **player.js**: Player logic
  - Playlist management
  - Song loading/playing
  - Auto-advance
  - Preloading
  - UI updates

## Technical Highlights

**Stable URLs:**
- Song IDs never change
- Safe to share and bookmark
- URLs survive file renaming

**No Dependencies:**
- Pure vanilla JavaScript
- No jQuery, React, Vue, etc.
- No build process needed
- Fast and lightweight

**Progressive Enhancement:**
- Works without JavaScript (redirects still work)
- Enhanced features when JavaScript enabled
- Mobile-first responsive design

**Free External Services:**
- QR Code API: https://api.qrserver.com/ (free, no signup)
- All other features are self-hosted

**SEO & Social:**
- Proper HTML structure
- Open Graph metadata on every page
- Twitter Card support
- Semantic HTML5

**Performance:**
- Lazy loading (only current song)
- Preloading next song
- Minified CSS (inline)
- No large dependencies
- CDN-free (all self-hosted)

## Browser Compatibility

**Tested and working:**
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (iOS and macOS)
- Mobile browsers (Chrome, Safari, Samsung Internet)

**Features:**
- Web Share API (mobile native sharing)
- Clipboard API (desktop sharing)
- HTML5 Audio (all modern browsers)
- CSS Grid/Flexbox (all modern browsers)

## File Sizes

- **index.html**: ~50-100 KB (depends on song count)
- **player.html**: ~10 KB
- **Each song stub**: ~1 KB
- **utils.js**: ~4 KB
- **search.js**: ~3.6 KB
- **player.js**: ~12 KB

**Total JavaScript**: ~20 KB (uncompressed)

## Maintenance Workflow

1. **Add songs**: Copy mp3/m4a to `docs/audio/{album}/`
2. **Scan**: `python scan_new_songs.py`
3. **Review**: Edit `songs_mapping.csv` (optional)
4. **Generate**: `python rebuild.py`
5. **Deploy**: `git add -A && git commit && git push`

Done! GitHub Pages auto-deploys.

## Future Enhancements (Not Yet Implemented)

Potential features for future:
- Shuffle playlist button
- Loop/repeat options
- Volume control
- Keyboard shortcuts
- Download song button (for local files)
- Favorites/bookmarks
- Recently played
- Search by artist/album
- Sort options (alphabetical, date added, etc.)
- Dark mode toggle
- Lyrics display
- Waveform visualization
- Audio equalizer

## Security & Privacy

- No user tracking
- No cookies
- No analytics (unless you add)
- No ads
- All audio files served from your domain
- QR API is public (doesn't store data)
- Open source code

## Credits

Built with:
- Python 3
- HTML5 + CSS3 + JavaScript
- QR Server API (https://goqr.me/)
- GitHub Pages (free hosting)
- Love for กาญจน์ลดา มฤคพิทักษ์'s music 🎵
