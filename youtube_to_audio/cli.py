import click
from youtube_to_audio.downloader import YouTubeDownloader
from pathlib import Path

@click.command()
@click.option("--url", type=str, default=None, help="YouTube video or playlist URL")
@click.option("--url-file", type=click.Path(exists=True), default=None, help="File containing YouTube URLs (one per line)")
@click.option("--format", "audio_format", type=click.Choice(["mp3", "wav", "flac", "aac", "ogg", "m4a", "opus"]), default="mp3", help="Audio format (default: mp3)")
@click.option("--output_name", type=str, default=None, help="Custom output file name (only for single videos)")
@click.option("--playlist_name", type=str, default=None, help="Custom folder name for playlist downloads")
@click.option("--debug", is_flag=True, help="Enable debug mode with verbose output")
def main(url, url_file, audio_format, output_name, playlist_name, debug):
    # Validate that either url or url_file is provided, but not both
    if not url and not url_file:
        click.secho("❌ Error: You must provide either --url or --url-file", fg="red", err=True)
        return

    if url and url_file:
        click.secho("❌ Error: Cannot use both --url and --url-file at the same time", fg="red", err=True)
        return

    # Collect URLs to process
    urls_to_process = []

    if url_file:
        # Read URLs from file
        try:
            with open(url_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        urls_to_process.append(line)

            if not urls_to_process:
                click.secho("❌ Error: No valid URLs found in file", fg="red", err=True)
                return

            click.secho(f"📋 Found {len(urls_to_process)} URL(s) to process", fg="cyan")
        except Exception as e:
            click.secho(f"❌ Error reading file: {e}", fg="red", err=True)
            return
    else:
        urls_to_process = [url]

    click.secho("🚀 Download Started! Please wait...", fg="green")

    downloader = YouTubeDownloader(audio_format, output_name, playlist_name, debug=debug)

    # Process each URL
    success_count = 0
    skip_count = 0
    error_count = 0

    for idx, current_url in enumerate(urls_to_process, 1):
        if len(urls_to_process) > 1:
            click.secho(f"\n[{idx}/{len(urls_to_process)}] Processing: {current_url}", fg="cyan")

        try:
            message = downloader.download_audio(current_url)
            # Use yellow for warnings, green for success
            if message.startswith("⚠️"):
                click.secho(message, fg="yellow")
                skip_count += 1
            else:
                click.secho(message, fg="green")
                success_count += 1
        except Exception as e:
            error_count += 1
            if debug:
                import traceback
                click.secho(f"❌ Error: {e}", fg="red", err=True)
                click.secho("Full traceback:", fg="red", err=True)
                click.echo(traceback.format_exc(), err=True)
            else:
                click.secho(f"❌ Error: {e}", fg="red", err=True)

    # Print summary if processing multiple URLs
    if len(urls_to_process) > 1:
        click.secho("\n" + "="*50, fg="cyan")
        click.secho("📊 Summary:", fg="cyan", bold=True)
        click.secho(f"  ✅ Successfully downloaded: {success_count}", fg="green")
        click.secho(f"  ⚠️  Skipped (already downloaded): {skip_count}", fg="yellow")
        click.secho(f"  ❌ Errors: {error_count}", fg="red")
        click.secho("="*50, fg="cyan")

if __name__ == "__main__":
    main()