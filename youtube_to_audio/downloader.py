import yt_dlp
import re
from pathlib import Path

class YouTubeDownloader:
    SUPPORTED_FORMATS = ["mp3", "wav", "flac", "aac", "ogg", "m4a", "opus"]
    URL_FILE_NAME = "Downloaded Videos URLs.txt"

    def __init__(self, audio_format: str = "mp3", output_name: str = None, playlist_name: str = None, debug: bool = False):
        if audio_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Invalid format! Choose between {', '.join(self.SUPPORTED_FORMATS)}.")
        self.audio_format = audio_format
        self.output_name = output_name
        self.playlist_name = playlist_name
        self.debug = debug
        self.url_file_path = self._get_url_file_path()
        self._ensure_url_file_exists()

    def _get_url_file_path(self) -> Path:
        """Get the path to the URL tracking file in the project root directory."""
        # Get the project root (parent of youtube_to_audio package)
        project_root = Path(__file__).parent.parent
        return project_root / self.URL_FILE_NAME

    def _ensure_url_file_exists(self):
        """Create the URL tracking file if it doesn't exist."""
        if not self.url_file_path.exists():
            self.url_file_path.touch()

    def _read_urls_from_file(self) -> set:
        """Read all URLs from the tracking file and return as a set."""
        urls = set()
        if self.url_file_path.exists():
            try:
                with open(self.url_file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        url = line.strip()
                        if url:  # Skip empty lines
                            urls.add(url)
            except Exception:
                pass  # If file read fails, return empty set
        return urls

    def _write_url_to_file(self, url: str):
        """Append a URL to the tracking file."""
        try:
            with open(self.url_file_path, 'a', encoding='utf-8') as f:
                f.write(url + '\n')
        except Exception:
            pass  # Silently fail if write fails

    def _is_url_downloaded(self, url: str) -> bool:
        """Check if a URL has already been downloaded."""
        downloaded_urls = self._read_urls_from_file()
        return url in downloaded_urls

    def _sanitize_folder_name(self, name: str) -> str:
        """Sanitize a string to be used as a folder name by removing invalid characters."""
        # Windows invalid characters: < > : " / \ | ? *
        invalid_chars = '<>:"/\\|?*'
        sanitized = name
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        # Replace multiple spaces/underscores with single underscore
        sanitized = re.sub(r'[_\s]+', '_', sanitized)
        return sanitized or 'Unknown_Playlist'

    def _is_playlist_url(self, url: str) -> bool:
        """
        Detect if a URL is a playlist.
        YouTube has multiple playlist URL formats:
        1. Direct playlist: https://www.youtube.com/playlist?list=...
        2. Video with playlist: https://www.youtube.com/watch?v=...&list=...
        3. Radio playlist: https://www.youtube.com/watch?v=...&list=...&start_radio=1
        """
        url_lower = url.lower()
        return (
            "playlist?" in url_lower or 
            "&list=" in url_lower or 
            "?list=" in url_lower
        )

    def download_audio(self, youtube_url: str):
        # Detect if URL is a playlist
        is_playlist = self._is_playlist_url(youtube_url)

        # Check if URL has already been downloaded
        if is_playlist:
            # For playlists, we'll check individual video URLs
            pass  # Will check individual videos below
        else:
            # For single videos, check the URL directly
            if self._is_url_downloaded(youtube_url):
                return f"⚠️ Video already downloaded. Skipping: {youtube_url}"

        if is_playlist:
            # Playlists go into "Playlist Downloads" folder, then into playlist-specific folder
            playlist_downloads_folder = "Playlist Downloads"
            playlist_folder = self.playlist_name or "%(playlist_title)s"
            output_template = f"{playlist_downloads_folder}/{playlist_folder}/%(title)s.%(ext)s"
        else:
            # Single videos go into "Single Downloads" folder
            single_downloads_folder = "Single Downloads"
            if self.output_name:
                output_template = f"{single_downloads_folder}/{self.output_name}.%(ext)s"
            else:
                output_template = f"{single_downloads_folder}/%(title)s.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': self.audio_format,
            'outtmpl': output_template,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': self.audio_format}],
            'quiet': not self.debug,  # Enable verbose output in debug mode
            'verbose': self.debug,    # Enable verbose logging in debug mode
            'noprogress': not self.debug,  # Show progress in debug mode
            'no_warnings': not self.debug,  # Show warnings in debug mode
            'yes_playlist': True,
        }

        try:
            if is_playlist:
                # For playlists, extract info first to get individual video URLs
                temp_ydl = yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True})
                info_dict = temp_ydl.extract_info(youtube_url, download=False)
                entries = info_dict.get('entries', [])
                
                if not entries:
                    raise RuntimeError("No videos found in playlist")
                
                downloaded_urls = self._read_urls_from_file()
                skipped_count = 0
                new_video_urls = []
                
                # Filter entries to only include videos that haven't been downloaded
                new_entries = []
                for entry in entries:
                    if entry:
                        video_url = entry.get('webpage_url') or entry.get('url')
                        if video_url:
                            if video_url in downloaded_urls:
                                skipped_count += 1
                            else:
                                new_entries.append(entry)
                                new_video_urls.append(video_url)
                
                # Check if all videos are already downloaded
                if not new_entries:
                    playlist_title_raw = self.playlist_name or info_dict.get('title', 'Unknown Playlist')
                    playlist_title_sanitized = self._sanitize_folder_name(playlist_title_raw)
                    return f"⚠️ All videos in playlist already downloaded. Skipping: Playlist Downloads/{playlist_title_sanitized}"
                
                # Get the actual playlist title to use in folder name
                playlist_title_raw = self.playlist_name or info_dict.get('title', 'Unknown Playlist')
                # Sanitize the playlist title for use as a folder name
                actual_playlist_title = self._sanitize_folder_name(playlist_title_raw)
                
                # Replace the template variable with actual playlist title
                # This is needed because when downloading individual videos, yt_dlp doesn't have playlist context
                # Structure: Playlist Downloads/Playlist Name/Video Title.ext
                actual_output_template = output_template.replace('%(playlist_title)s', actual_playlist_title)
                ydl_opts['outtmpl'] = actual_output_template
                
                # Download only new videos
                # Create a list of URLs to download
                urls_to_download = [entry.get('webpage_url') or entry.get('url') for entry in new_entries if entry]
                
                downloaded_count = 0
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    for video_url in urls_to_download:
                        if video_url:
                            try:
                                ydl.download([video_url])
                                # Add URL to tracking file after successful download
                                self._write_url_to_file(video_url)
                                downloaded_count += 1
                            except Exception as e:
                                # Continue with next video if one fails
                                if self.debug:
                                    print(f"Failed to download {video_url}: {e}")
                                continue
                
                # Use the sanitized playlist title for the message (same as folder name)
                message = f"✅ Playlist download complete! Saved in folder: 'Playlist Downloads/{actual_playlist_title}'. "
                message += f"Downloaded {downloaded_count} new video(s)"
                if skipped_count > 0:
                    message += f", skipped {skipped_count} already downloaded video(s)"
                message += "."
                return message
            
            # Single video download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(youtube_url, download=True)
                video_title = self.output_name or info_dict.get('title', 'Unknown Video')
                
                # Add URL to tracking file after successful download
                self._write_url_to_file(youtube_url)
                
                return f"✅ Download complete! Saved in 'Single Downloads' folder as '{video_title}.{self.audio_format}'."

        except Exception as e:
            raise RuntimeError(f"❌ Error downloading audio: {e}")