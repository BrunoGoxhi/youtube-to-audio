# IDE Setup Guide for YouTube-to-Audio

## Virtual Environment Configuration

**Important:** You don't need to manually activate the venv when debugging in an IDE. The IDE will automatically use the venv's Python interpreter once configured.

---

## VS Code Setup

### Method 0: Install Package in Editable Mode (BEST SOLUTION)
This installs your package so Python can find it anywhere:

1. Activate your venv in terminal:
   ```powershell
   D:\venvs\youtube-to-audio\Scripts\Activate.ps1
   ```

2. Install in editable mode:
   ```powershell
   pip install -e .
   ```

3. Now your IDE will find the package automatically!

### Method 1: Select Interpreter (Recommended)
1. Open the project in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Python: Select Interpreter"
4. Choose: `D:\venvs\youtube-to-audio\Scripts\python.exe`

### Method 2: Create `.vscode/settings.json`
Create `.vscode/settings.json` in your project root:
```json
{
    "python.defaultInterpreterPath": "D:\\venvs\\youtube-to-audio\\Scripts\\python.exe",
    "python.terminal.activateEnvironment": true
}
```

### Method 3: Create Launch Configuration (Fixes ModuleNotFoundError)
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: YouTube-to-Audio CLI (Module)",
            "type": "python",
            "request": "launch",
            "module": "youtube_to_audio.cli",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "args": [
                "--url",
                "YOUR_URL_HERE"
            ],
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: YouTube-to-Audio CLI (Direct)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/youtube_to_audio/cli.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "args": [
                "--url",
                "YOUR_URL_HERE"
            ],
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

**Important:** The `PYTHONPATH` environment variable tells Python where to find your package!

**To Debug:**
1. Set breakpoints (click left of line numbers)
2. Press `F5` or click "Run and Debug"
3. Select your configuration

---

## PyCharm Setup

### Method 1: Configure Project Interpreter
1. Go to `File` → `Settings` (or `PyCharm` → `Preferences` on Mac)
2. Navigate to `Project: youtube-to-audio` → `Python Interpreter`
3. Click the gear icon → `Add...`
4. Select `Existing environment`
5. Browse to: `D:\venvs\youtube-to-audio\Scripts\python.exe`
6. Click `OK`

### Method 2: Create Run Configuration
1. Go to `Run` → `Edit Configurations...`
2. Click `+` → `Python`
3. Set:
   - **Name:** YouTube-to-Audio CLI
   - **Script path:** `youtube_to_audio/cli.py`
   - **Python interpreter:** `D:\venvs\youtube-to-audio\Scripts\python.exe`
   - **Parameters:** `--url "YOUR_URL_HERE"`
   - **Working directory:** Project root

**To Debug:**
1. Set breakpoints
2. Right-click on `cli.py` → `Debug 'cli'`
   OR
   Click the debug icon (bug) next to the run configuration

---

## General IDE Tips

### Verify Venv is Active
In VS Code, check the bottom-right corner - it should show:
```
Python 3.12.x ('youtube-to-audio': venv)
```

In PyCharm, check the status bar - it should show the venv path.

### If Packages Aren't Found
1. **VS Code:** Reload window (`Ctrl+Shift+P` → "Developer: Reload Window")
2. **PyCharm:** Invalidate caches (`File` → `Invalidate Caches...`)

### Terminal in IDE
- **VS Code:** The integrated terminal will automatically activate the venv
- **PyCharm:** The terminal will show `(youtube-to-audio)` prefix when venv is active

---

## Quick Test

Create a simple test to verify venv is working:

```python
# test_venv.py
import sys
print(f"Python: {sys.executable}")
print(f"yt_dlp installed: {__import__('yt_dlp') is not None}")
```

Run this in your IDE - it should show the venv path, not system Python.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'youtube_to_audio'"
**This is the error you're experiencing!**

**Solution 1 (Recommended):** Install package in editable mode
```powershell
# Activate venv
D:\venvs\youtube-to-audio\Scripts\Activate.ps1

# Install in editable mode
pip install -e .
```

**Solution 2:** Use the launch.json configuration I created
- The `.vscode/launch.json` file includes `PYTHONPATH` environment variable
- Use the "Python: YouTube-to-Audio CLI (Module)" configuration
- This tells Python where to find your package

**Solution 3:** Manually set PYTHONPATH in VS Code settings
Add to `.vscode/settings.json`:
```json
{
    "python.envFile": "${workspaceFolder}/.env"
}
```
Create `.env` file:
```
PYTHONPATH=${workspaceFolder}
```

### Issue: "ModuleNotFoundError: No module named 'yt_dlp'"
**Solution:** IDE is using wrong Python interpreter
- VS Code: Select correct interpreter (`Ctrl+Shift+P` → "Python: Select Interpreter")
- PyCharm: Configure project interpreter (see above)

### Issue: Breakpoints not working
**Solution:** 
- Ensure "Just My Code" is disabled in debug settings
- Check that you're debugging, not just running

### Issue: Changes not reflecting
**Solution:**
- Restart IDE
- Reload window (VS Code)
- Invalidate caches (PyCharm)

