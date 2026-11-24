"""
Stream Ingestion and Video Slicing Module.
Uses yt-dlp to extract stream metadata, chat comments, and subtitles,
and FFmpeg for ultra-fast direct stream slicing.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

FFMPEG_BIN = r"C:\ffmpeg\bin\ffmpeg.exe" if os.path.exists(r"C:\ffmpeg\bin\ffmpeg.exe") else "ffmpeg"
FFPROBE_BIN = r"C:\ffmpeg\bin\ffprobe.exe" if os.path.exists(r"C:\ffmpeg\bin\ffprobe.exe") else "ffprobe"


def get_stream_metadata(url, work_dir):
    """
    Extracts stream metadata, subtitles, and comments into work_dir.
    Returns metadata dict, subtitles path, and comments path.
    """
    work_path = Path(work_dir)
    work_path.mkdir(parents=True, exist_ok=True)
    meta_json_path = work_path / "metadata.json"
    comments_json_path = work_path / "comments.info.json"
    subs_pattern = work_path / "subs"

    print(f"[Downloader] Fetching video metadata and stream links for: {url}")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--dump-json",
        "--skip-download",
        "--no-playlist",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"yt-dlp metadata failed: {res.stderr}")

    meta = json.loads(res.stdout)
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    # Subtitles extraction
    print("[Downloader] Extracting auto-captions and subtitles...")
    subs_cmd = [
        sys.executable, "-m", "yt_dlp",
        "--write-auto-subs", "--write-subs",
        "--sub-langs", "hi-orig,hi,en,en-orig",
        "--sub-format", "vtt",
        "--skip-download",
        "-o", str(subs_pattern),
        url
    ]
    subprocess.run(subs_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    # Find the best subtitle file
    sub_file = None
    for ext in [".hi-orig.vtt", ".hi.vtt", ".en-orig.vtt", ".en.vtt", ".vtt"]:
        candidates = list(work_path.glob(f"*{ext}"))
        if candidates:
            sub_file = str(candidates[0])
            break

    # Comments / live chat extraction (capped to 2000 comments for speed)
    print("[Downloader] Fetching chat and audience reaction comments...")
    comments_cmd = [
        sys.executable, "-m", "yt_dlp",
        "--write-comments",
        "--extractor-args", "youtube:max_comments=2000",
        "--skip-download",
        "-o", str(work_path / "%(id)s"),
        url
    ]
    subprocess.run(comments_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    comment_candidates = list(work_path.glob("*.info.json"))
    comment_file = str(comment_candidates[0]) if comment_candidates else None

    # Extract direct HLS / mp4 stream URLs for fast seeking
    print("[Downloader] Resolving direct media stream URLs...")
    stream_url_cmd = [
        sys.executable, "-m", "yt_dlp",
        "-g",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        url
    ]
    url_res = subprocess.run(stream_url_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    direct_urls = [u.strip() for u in url_res.stdout.strip().splitlines() if u.strip()]

    stream_info = {
        "id": meta.get("id"),
        "title": meta.get("title"),
        "uploader": meta.get("uploader"),
        "duration": meta.get("duration"),
        "thumbnail": meta.get("thumbnail"),
        "meta_file": str(meta_json_path),
        "subs_file": sub_file,
        "comments_file": comment_file,
        "direct_urls": direct_urls,
        "raw_meta": meta
    }
    return stream_info


def slice_stream(direct_urls, start_seconds, duration_seconds, output_path):
    """
    Slices stream directly using FFmpeg without downloading the entire video.
    direct_urls can be [video_url, audio_url] or a single combined url.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[Downloader] Slicing {duration_seconds}s segment from {start_seconds}s -> {output_path.name}...")

    if len(direct_urls) == 2:
        v_url, a_url = direct_urls[0], direct_urls[1]
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", str(start_seconds),
            "-t", str(duration_seconds),
            "-i", v_url,
            "-ss", str(start_seconds),
            "-t", str(duration_seconds),
            "-i", a_url,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            str(output_path)
        ]
    else:
        url = direct_urls[0]
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", str(start_seconds),
            "-t", str(duration_seconds),
            "-i", url,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            str(output_path)
        ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg slicing failed: {res.stderr}")

    print(f"[Downloader] Slice complete: {output_path} ({os.path.getsize(output_path)/(1024*1024):.2f} MB)")
    return str(output_path)

