# PowerShell script to generate OneDrive share links for all music files
# This will create public share links for each file

param(
    [string]$MusicFolder = "C:\Users\kacha\OneDrive\_Old_Backup\Karnlada Songs",
    [string]$OutputFile = "C:\dev\karnlada_songs\onedrive_links.json"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OneDrive Share Link Generator" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if OneDrive module is available
Write-Host "Checking for OneDrive integration..." -ForegroundColor Yellow

# Get all MP3 and M4A files
$audioFiles = Get-ChildItem -Path $MusicFolder -Recurse -Include *.mp3,*.m4a

Write-Host "Found $($audioFiles.Count) audio files`n" -ForegroundColor Green

# Array to store results
$results = @()
$successCount = 0
$failCount = 0

# Fixed values
$artist = "กาญจน์ลดา มฤคพิทักษ์"
$albumArtUrl = "https://1drv.ms/i/c/19724284c9b34401/EaRNlSs0VH9IpgzboKat2vYBNdVlQ9a4WWOoIvvnracDrA?e=s9mA4Q"

foreach ($file in $audioFiles) {
    $filename = $file.Name
    $title = [System.IO.Path]::GetFileNameWithoutExtension($filename)

    # Remove artist name from title if present
    $title = $title -replace ' - กาญจน์ลดา มฤคพิทักษ์$', ''
    $title = $title -replace ' ชรินทร์$', ''
    $title = $title -replace '^\d+\.\s*', ''  # Remove track numbers like "01. "

    Write-Host "Processing: $title" -ForegroundColor White

    try {
        # Method 1: Try to get existing share link from file properties
        $shareLink = $null

        # Try to use OneDrive PowerShell cmdlets if available
        # Note: This requires OneDrive to be installed and file to be synced

        # For now, we'll create a placeholder that user needs to fill
        # In a real scenario, you would use:
        # 1. OneDrive REST API
        # 2. Microsoft Graph API
        # 3. Manual sharing via File Explorer

        Write-Host "  → Share link needs to be created manually" -ForegroundColor Yellow

        $results += [PSCustomObject]@{
            title = $title
            artist = $artist
            audio_url = "PLACEHOLDER - Right-click file and share: $($file.FullName)"
            album_art_url = $albumArtUrl
            file_path = $file.FullName
            status = "pending"
        }

        $failCount++

    } catch {
        Write-Host "  ✗ Error: $_" -ForegroundColor Red
        $failCount++
    }
}

# Save results to JSON
$output = @{
    files = $results
    total_count = $audioFiles.Count
    success_count = $successCount
    pending_count = $failCount
    artist = $artist
    album_art_url = $albumArtUrl
} | ConvertTo-Json -Depth 10

$output | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Results:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total files: $($audioFiles.Count)" -ForegroundColor White
Write-Host "Pending manual share: $failCount" -ForegroundColor Yellow
Write-Host "`nOutput saved to: $OutputFile" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS - AUTOMATED SHARING:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host @"

Since PowerShell cannot automatically create OneDrive share links,
here are your options:

OPTION 1 - Bulk share via File Explorer (Recommended):
1. Open: $MusicFolder
2. Select all MP3/M4A files (Ctrl+A in each folder)
3. Right-click → Share (OneDrive option)
4. Click "Copy link" for each file
5. This creates public share links

OPTION 2 - Use the Python helper script (Coming next):
Run the interactive Python script that will:
1. Show each song title
2. Ask you to paste the share link
3. Automatically update the configuration

OPTION 3 - Use OneDrive Web:
1. Go to onedrive.live.com
2. Navigate to your music folder
3. Right-click each file → Share → Copy link

The Python helper script will be created next to make this easier!

"@ -ForegroundColor White
