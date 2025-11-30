# FFmpeg Installation Script
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$downloadPath = Join-Path $env:TEMP "ffmpeg.zip"
$extractPath = "D:\Program Files\ffmpeg"
$binPath = "D:\Program Files\ffmpeg\bin"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FFmpeg Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Download FFmpeg
Write-Host "Step 1: Downloading FFmpeg..." -ForegroundColor Yellow
Write-Host "URL: $ffmpegUrl" -ForegroundColor Gray
Write-Host "This may take a few minutes depending on your internet connection..." -ForegroundColor Gray

try {
    Invoke-WebRequest -Uri $ffmpegUrl -OutFile $downloadPath -UseBasicParsing
    Write-Host "[OK] Download complete!" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Extract FFmpeg
Write-Host ""
Write-Host "Step 2: Extracting FFmpeg to $extractPath..." -ForegroundColor Yellow

# Remove existing directory if it exists
if (Test-Path $extractPath) {
    Write-Host "Removing existing installation..." -ForegroundColor Gray
    Remove-Item -Path $extractPath -Recurse -Force
}

# Create extraction directory
New-Item -ItemType Directory -Force -Path $extractPath | Out-Null

try {
    # Extract the zip file
    Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force
    
    # The zip contains a folder like "ffmpeg-6.x-essentials_build", we need to move contents up one level
    $extractedFolders = Get-ChildItem -Path $extractPath -Directory
    if ($extractedFolders.Count -eq 1) {
        $innerFolder = $extractedFolders[0].FullName
        Write-Host "Moving files from subdirectory..." -ForegroundColor Gray
        Get-ChildItem -Path $innerFolder | Move-Item -Destination $extractPath -Force
        Remove-Item -Path $innerFolder -Force
    }
    
    Write-Host "[OK] Extraction complete!" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Extraction failed: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Add to PATH
Write-Host ""
Write-Host "Step 3: Adding FFmpeg to PATH..." -ForegroundColor Yellow

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$binPath*") {
    $newPath = $currentPath + ";$binPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "[OK] Added to PATH: $binPath" -ForegroundColor Green
    Write-Host "  Note: You may need to restart your terminal for PATH changes to take effect." -ForegroundColor Yellow
} else {
    Write-Host "[OK] FFmpeg is already in PATH" -ForegroundColor Green
}

# Step 4: Cleanup
Write-Host ""
Write-Host "Step 4: Cleaning up temporary files..." -ForegroundColor Yellow
Remove-Item -Path $downloadPath -Force -ErrorAction SilentlyContinue
Write-Host "[OK] Cleanup complete!" -ForegroundColor Green

# Step 5: Verify installation
Write-Host ""
Write-Host "Step 5: Verifying installation..." -ForegroundColor Yellow
$ffmpegExe = Join-Path $binPath "ffmpeg.exe"
if (Test-Path $ffmpegExe) {
    Write-Host "[OK] FFmpeg installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installation Summary:" -ForegroundColor Cyan
    Write-Host "  Location: $extractPath" -ForegroundColor White
    Write-Host "  Binary Path: $binPath" -ForegroundColor White
    Write-Host ""
    Write-Host "To verify FFmpeg is working, restart your terminal and run:" -ForegroundColor Yellow
    Write-Host "  ffmpeg -version" -ForegroundColor White
} else {
    Write-Host "[ERROR] FFmpeg executable not found at expected location" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
