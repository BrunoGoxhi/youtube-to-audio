from setuptools import setup, find_packages

setup(
    name="youtube-to-audio",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp>=2023.12.30",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "youtube-to-audio=youtube_to_audio.cli:main",
        ],
    },
)

