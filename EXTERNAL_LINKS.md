# Adding External Links (YouTube, SoundCloud, etc.)

The system now supports adding external links alongside local audio files. This allows you to link to songs on YouTube, SoundCloud, or other platforms.

## How to Add an External Link

1. **Open `songs_mapping.csv`** in a text editor or spreadsheet program

2. **Add a new row** with the following format:
   ```csv
   song_id,album,title,artist,audio_file_path,html_filename,is_external
   abc123de,External Links,Song Title,กาญจน์ลดา มฤคพิทักษ์,https://youtube.com/watch?v=xyz,abc123de.html,true
   ```

   Fields explained:
   - `song_id`: Generate a unique 8-character ID (letters/numbers). Keep it short and unique.
   - `album`: Album name (can be a virtual album like "YouTube" or "External Links")
   - `title`: Song title in Thai
   - `artist`: Artist name (default: กาญจน์ลดา มฤคพิทักษ์)
   - `audio_file_path`: **The full external URL** (YouTube, SoundCloud, etc.)
   - `html_filename`: Same as song_id with `.html` extension (e.g., `abc123de.html`)
   - `is_external`: **Must be `true`** for external links

3. **Run the rebuild script** to generate the pages:
   ```bash
   python rebuild.py
   ```

4. **Commit and push** to deploy:
   ```bash
   git add -A
   git commit -m "Add external link for [Song Name]"
   git push
   ```

## Example

To add a YouTube link:

```csv
yt123456,YouTube,เพลงตัวอย่าง,กาญจน์ลดา มฤคพิทักษ์,https://www.youtube.com/watch?v=dQw4w9WgXcQ,yt123456.html,true
```

This will create:
- URL: `https://kacharuk.github.io/karnlada_songs/songs/yt123456.html`
- When users click the link, they'll be redirected to the YouTube video
- The link will appear in the index organized by the "YouTube" album

## Mixing Local and External

You can have both local audio files and external links in the same playlist. The system handles them automatically:

- **Local files** (`is_external=false`): Play in the custom web player
- **External links** (`is_external=true`): Redirect directly to the external URL

## Album Art for External Links

External links use the default album art (`images/album_art_karnlada.jpg`). If you want custom album art:

1. Create an album folder: `docs/audio/[Album Name]/`
2. Add `album_art.jpg` to that folder
3. Update the CSV with the album name

## Notes

- **Stable IDs**: Once you assign a song_id, don't change it. The ID makes the URL permanent.
- **URL Format**: External URLs must be complete (including `https://`)
- **Platform Support**: Works with any platform that accepts direct links (YouTube, SoundCloud, Spotify, etc.)
- **Social Sharing**: Open Graph metadata will still work for previews when sharing the link

## Troubleshooting

**Q: The external link doesn't appear in the index**
A: Make sure you ran `python rebuild.py` after editing the CSV

**Q: The link goes to the player instead of YouTube**
A: Check that `is_external` is set to `true` (lowercase) in the CSV

**Q: Can I change the external URL later?**
A: Yes! Just edit the `audio_file_path` in the CSV and rebuild. The song_id stays the same, so shared links still work.
