#!/usr/bin/env python3
"""
Test script to verify playlist URL detection works correctly
"""

from youtube_to_audio.downloader import YouTubeDownloader

def test_playlist_detection():
    """Test various playlist URL formats"""
    
    downloader = YouTubeDownloader()
    
    test_urls = [
        # Direct playlist URL
        ("https://www.youtube.com/playlist?list=PLRBp0Fe2GpgnymQGm0yIxcdzkQsPKwnBD", True),
        
        # Video URL with playlist parameter (your case)
        ("https://www.youtube.com/watch?v=QFs3PIZb3js&list=RDQFs3PIZb3js&start_radio=1", True),
        
        # Radio playlist
        ("https://www.youtube.com/watch?v=VIDEO_ID&list=RDVIDEO_ID&start_radio=1", True),
        
        # Single video (no playlist)
        ("https://www.youtube.com/watch?v=QFs3PIZb3js", False),
        
        # Video with other parameters but no list
        ("https://www.youtube.com/watch?v=VIDEO_ID&t=123", False),
    ]
    
    print("=" * 70)
    print("Testing Playlist URL Detection")
    print("=" * 70)
    print()
    
    all_passed = True
    for url, expected_is_playlist in test_urls:
        result = downloader._is_playlist_url(url)
        status = "✅ PASS" if result == expected_is_playlist else "❌ FAIL"
        
        if result != expected_is_playlist:
            all_passed = False
        
        print(f"{status} | Expected: {expected_is_playlist}, Got: {result}")
        print(f"   URL: {url[:60]}...")
        print()
    
    print("=" * 70)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 70)

if __name__ == "__main__":
    test_playlist_detection()

