# Debugging Guide for YouTube-to-Audio

This guide covers various methods to debug the YouTube-to-Audio application.

## 1. Using Python Debugger (pdb)

### Method 1: Add breakpoints in code
Add this line where you want to pause execution:
```python
import pdb; pdb.set_trace()
```

### Method 2: Run with debugger from command line
```bash
python -m pdb -m youtube_to_audio.cli --url "YOUR_URL"
```

### Method 3: Post-mortem debugging (after exception)
Add to `cli.py`:
```python
import pdb
try:
    message = downloader.download_audio(url)
except Exception as e:
    pdb.post_mortem()
    raise
```

## 2. Enable Verbose Logging

### Option A: Add logging to the code
The code already has some error handling. You can enhance it by adding logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Option B: Enable yt_dlp verbose output
Modify `downloader.py` to set `'quiet': False` and `'verbose': True` in `ydl_opts`.

## 3. Using IDE Debugger (VS Code, PyCharm, etc.)

### VS Code:
1. Set breakpoints by clicking left of line numbers
2. Press F5 or go to Run > Start Debugging
3. Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": ["--url", "YOUR_URL"]
        }
    ]
}
```

### PyCharm:
1. Right-click on `cli.py` > Debug 'cli'
2. Set breakpoints and configure run arguments

## 4. Add Debug Mode Flag

Run with `--debug` flag to enable verbose output:
```bash
python -m youtube_to_audio.cli --url "YOUR_URL" --debug
```

## 5. Test Individual Components

### Test URL tracking:
```python
from youtube_to_audio.downloader import YouTubeDownloader

downloader = YouTubeDownloader()
print(f"URL file path: {downloader.url_file_path}")
print(f"Downloaded URLs: {downloader._read_urls_from_file()}")
```

### Test single method:
```python
downloader = YouTubeDownloader()
# Test if URL is downloaded
print(downloader._is_url_downloaded("https://youtube.com/watch?v=..."))
```

## 6. Common Debugging Scenarios

### Issue: FFmpeg not found
- Check: `ffmpeg -version` in terminal
- Verify PATH includes FFmpeg bin directory

### Issue: URL tracking not working
- Check: File exists at project root
- Check: File permissions (read/write)
- Verify: URLs are being written correctly

### Issue: Playlist downloads failing
- Enable verbose mode in yt_dlp
- Check: Individual video URLs are valid
- Verify: match_filter is working correctly

### Issue: Download fails silently
- Check: Exception handling in code
- Add: More detailed error messages
- Enable: yt_dlp verbose output

## 7. Quick Debug Script

Create `test_debug.py`:
```python
from youtube_to_audio.downloader import YouTubeDownloader
import traceback

try:
    downloader = YouTubeDownloader()
    result = downloader.download_audio("YOUR_URL_HERE")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
```

## 8. Enable yt_dlp Debug Output

Temporarily modify `downloader.py`:
```python
ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': self.audio_format,
    'outtmpl': output_template,
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': self.audio_format}],
    'quiet': False,        # Changed from True
    'verbose': True,        # Add this
    'noprogress': False,   # Changed from True to see progress
    'no_warnings': False,  # Changed from True to see warnings
    'yes_playlist': True,
}
```

