# How to Get Working OneDrive Links

The issue is that neither preview links (1drv.ms) nor API links work without authentication for direct embedding.

## Solution: Use OneDrive Embed URLs

### For Audio Files:

1. Go to **https://onedrive.live.com**
2. Navigate to your audio file
3. **Right-click** → **Embed**
4. You'll see something like:
   ```html
   <iframe src="https://onedrive.live.com/embed?resid=CID%21RESID&authkey=!..." ...></iframe>
   ```
5. **Copy the full URL from the src attribute**

### For Album Art (Images):

Same process:
1. Right-click image → **Embed**
2. Copy the iframe src URL

### Alternative: Use Download Links

If Embed doesn't work:

1. Right-click file → **Download**
2. Open browser Developer Tools (F12) → Network tab
3. Click Download
4. Copy the actual download URL from the network request
5. It will look like:
   ```
   https://public.am.files.1drv.com/...
   ```

## Quick Test

Let me create a test page where you can paste one working URL to verify it works before updating all files.
