# How to Get Direct Download URLs from OneDrive

The embed URLs from OneDrive (https://1drv.ms/...) don't work for direct embedding in HTML5 audio/img tags.

## Method: Get Real Download URLs

### For Audio Files:

1. Go to **https://onedrive.live.com**
2. Find your audio file
3. Right-click → **Download**
4. **Before the download starts**, open Browser Developer Tools:
   - Chrome/Edge: Press **F12**
   - Go to **Network** tab
   - Make sure recording is on (red dot)
5. Click Download again
6. In the Network tab, look for the request (usually the filename)
7. **Right-click** on that request → **Copy** → **Copy URL**
8. That URL will look like:
   ```
   https://public.am.files.1drv.com/y4m...
   ```
   OR
   ```
   https://xyz.sharepoint.com/...
   ```

### For Images:

Same process - right-click → Download → copy URL from Network tab

## Alternative: Test with Direct URL Construction

OneDrive sometimes allows this format:
```
https://onedrive.live.com/download?resid=CID%21RESID&authkey=AUTHKEY
```

Let me create a helper that tries to construct this from your share links.
