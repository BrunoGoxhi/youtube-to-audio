#!/usr/bin/env python3
"""
Simple debug script for testing YouTube-to-Audio functionality
Usage: python test_debug.py [URL]
"""

import sys
from youtube_to_audio.downloader import YouTubeDownloader
import traceback

def test_url_tracking():
    """Test URL tracking functionality"""
    print("=" * 50)
    print("Testing URL Tracking")
    print("=" * 50)
    
    downloader = YouTubeDownloader()
    print(f"URL file path: {downloader.url_file_path}")
    print(f"File exists: {downloader.url_file_path.exists()}")
    
    urls = downloader._read_urls_from_file()
    print(f"Downloaded URLs count: {len(urls)}")
    if urls:
        print("Downloaded URLs:")
        for url in list(urls)[:5]:  # Show first 5
            print(f"  - {url}")
        if len(urls) > 5:
            print(f"  ... and {len(urls) - 5} more")
    print()

def test_download(url, debug=False):
    """Test downloading a video"""
    print("=" * 50)
    print(f"Testing Download: {url}")
    print("=" * 50)
    
    try:
        downloader = YouTubeDownloader(debug=debug)
        
        # Check if already downloaded
        is_downloaded = downloader._is_url_downloaded(url)
        print(f"Already downloaded: {is_downloaded}")
        
        if not is_downloaded:
            print("Starting download...")
            result = downloader.download_audio(url)
            print(f"Result: {result}")
        else:
            print("Skipping download (already exists)")
            
    except Exception as e:
        print(f"ERROR: {e}")
        if debug:
            traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_debug.py [URL] [--debug]")
        print("\nOr run without URL to test URL tracking:")
        test_url_tracking()
        return
    
    url = sys.argv[1]
    debug = "--debug" in sys.argv
    
    if debug:
        print("DEBUG MODE ENABLED")
        print()
    
    test_url_tracking()
    test_download(url, debug=debug)

if __name__ == "__main__":
    main()

