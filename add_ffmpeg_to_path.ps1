# Script to add FFmpeg to PATH
$ffmpegBasePath = "D:\Program Files\ffmpeg-2025-11-24-git-c732564d2e-full_build"
$binPath = Join-Path $ffmpegBasePath "bin"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Adding FFmpeg to PATH" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if FFmpeg folder exists
if (-not (Test-Path $ffmpegBasePath)) {
    Write-Host "[ERROR] FFmpeg folder not found at: $ffmpegBasePath" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] FFmpeg folder found: $ffmpegBasePath" -ForegroundColor Green

# Check for bin folder
if (-not (Test-Path $binPath)) {
    Write-Host "[WARNING] Bin folder not found at: $binPath" -ForegroundColor Yellow
    Write-Host "Checking folder structure..." -ForegroundColor Yellow
    Get-ChildItem $ffmpegBasePath | Select-Object Name, PSIsContainer | Format-Table
    
    # Try to find ffmpeg.exe directly in the base folder
    $ffmpegExe = Get-ChildItem -Path $ffmpegBasePath -Filter "ffmpeg.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($ffmpegExe) {
        $binPath = $ffmpegExe.DirectoryName
        Write-Host "[OK] Found ffmpeg.exe at: $binPath" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Could not find ffmpeg.exe" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] Bin folder found: $binPath" -ForegroundColor Green
}

# Verify ffmpeg.exe exists
$ffmpegExe = Join-Path $binPath "ffmpeg.exe"
if (-not (Test-Path $ffmpegExe)) {
    Write-Host "[ERROR] ffmpeg.exe not found at: $ffmpegExe" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] ffmpeg.exe verified at: $ffmpegExe" -ForegroundColor Green
Write-Host ""

# Add to PATH
Write-Host "Adding to PATH..." -ForegroundColor Yellow
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -like "*$binPath*") {
    Write-Host "[INFO] FFmpeg is already in PATH" -ForegroundColor Yellow
} else {
    $newPath = $currentPath + ";$binPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "[OK] Added to PATH: $binPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: You need to restart your terminal/PowerShell window" -ForegroundColor Yellow
    Write-Host "for the PATH changes to take effect." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "After restarting your terminal, verify installation with:" -ForegroundColor Yellow
Write-Host "  ffmpeg -version" -ForegroundColor White
Write-Host ""

