"""
Video Rendering & Compositing Module.
Renders high-definition vertical (1080x1920 @ 60 FPS) reels with:
- Top facecam & bottom gameplay split
- Animated ASS typography overlay
- EBU R128 (-16 LUFS) audio loudness normalization
- High-res cover thumbnail extraction
"""

import os
import subprocess
from pathlib import Path

FFMPEG_BIN = r"C:\ffmpeg\bin\ffmpeg.exe" if os.path.exists(r"C:\ffmpeg\bin\ffmpeg.exe") else "ffmpeg"


def render_vertical_reel(raw_clip_path, ass_path, layout_cfg, output_mp4_path, thumb_path=None):
    """
    Renders raw video clip into 9:16 vertical MP4 with subtitles and audio normalization.
    """
    output_mp4_path = Path(output_mp4_path)
    output_mp4_path.parent.mkdir(parents=True, exist_ok=True)

    # Windows FFmpeg colon escaping for filtergraph
    # C:/path or D:/path needs escaped colon like D\:/path
    escaped_ass = str(ass_path).replace("\\", "/").replace(":", "\\:")

    has_cam = layout_cfg.get("has_facecam", False)
    cam_crop = layout_cfg.get("facecam_crop")
    gameplay_crop = layout_cfg.get("gameplay_crop", "crop=1200:in_h:360:0")

    if has_cam and cam_crop:
        filter_str = (
            f"[0:v]{cam_crop},scale=1080:720:force_original_aspect_ratio=increase,crop=1080:720[cam];"
            f"[0:v]{gameplay_crop},scale=1080:1200:force_original_aspect_ratio=increase,crop=1080:1200[game];"
            f"[cam][game]vstack=inputs=2[vstacked];"
            f"[vstacked]ass=filename='{escaped_ass}'[vout]"
        )
    else:
        # Full gameplay vertical presentation with blurred letterbox background
        filter_str = (
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
            f"[0:v]scale=1080:608[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[vbase];"
            f"[vbase]ass=filename='{escaped_ass}'[vout]"
        )

    print(f"[ReelRenderer] Rendering vertical composition -> {output_mp4_path.name}...")
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", str(raw_clip_path),
        "-filter_complex", filter_str,
        "-map", "[vout]",
        "-map", "0:a?",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "60",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        str(output_mp4_path)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg render failed: {res.stderr}")

    file_size_mb = os.path.getsize(output_mp4_path) / (1024 * 1024)
    print(f"[ReelRenderer] Render successful: {output_mp4_path} ({file_size_mb:.2f} MB)")

    # Extract high-impact thumbnail at 35% timestamp
    if thumb_path:
        extract_thumbnail(output_mp4_path, thumb_path)

    return str(output_mp4_path)


def extract_thumbnail(video_path, thumb_output_path, timestamp_sec=15.0):
    """Extracts a high-definition frame to serve as cover / thumbnail."""
    thumb_path = Path(thumb_output_path)
    thumb_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        FFMPEG_BIN, "-y",
        "-ss", str(timestamp_sec),
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(thumb_path)
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    if thumb_path.exists():
        print(f"[ReelRenderer] Cover thumbnail extracted: {thumb_path.name}")
    return str(thumb_path)

