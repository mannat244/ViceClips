# Stream Reel Studio

An automated pipeline for extracting high-retention vertical clips (9:16) from gaming streams and long-form videos, managing review workflows, and publishing directly to Instagram Reels and YouTube Shorts.

## Highlights

- **Fast Stream Clipping**: Extracts targeted segments via direct stream seeking using FFmpeg without downloading multi-hour streams.
- **Dynamic Vertical Composition**: Automatically separates streamer facecam and gameplay into an optimized 9:16 layout (1080x1920 @ 60 FPS).
- **Word-Synced Captions**: Generates animated subtitle overlays with custom color highlights based on audio/caption timing.
- **Audio Mastering**: Normalizes dialogue and gameplay sound to broadcast loudness standards (-16 LUFS).
- **Approval Workflow**: Tracks clip states (`pending_approval`, `approved`, `posted`) in structured manifests.
- **Multi-Platform Publishing**: Direct 1-click uploads to YouTube Shorts (via Google Data API v3) and Instagram Reels (via Meta Graph API).

---

## Architecture

```
YouTube URL ──> Slicing & Detection ──> Vertical Render ──> Approval Gate ──> Social Publish
```

### Directory Structure

```
.
├── .agents/skills/stream-reel-studio/   # Antigravity skill definition
├── config/                             # Configuration files & credential templates
│   └── publisher_config.example.json
├── pipeline/                           # Core modular pipeline
│   ├── downloader.py                   # Stream metadata & slicing
│   ├── layout_detector.py              # Facecam & gameplay detection
│   ├── moment_detector.py              # Highlight discovery
│   ├── subtitle_styler.py              # ASS karaoke subtitle generation
│   ├── reel_renderer.py                # Vertical video compositor
│   ├── approval_manager.py             # Manifest & status management
│   └── publisher.py                    # Social media upload engines
├── clips/                              # Rendered video deliverables
├── clip_master.py                      # Unified CLI entry point
├── auto_publisher.py                   # Social posting engine
├── Publish_Reels.bat                   # Windows interactive launcher
├── pyproject.toml                      # Package installation spec
└── requirements.txt                    # Python dependencies
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- FFmpeg installed and available on PATH (or at `C:\ffmpeg\bin\ffmpeg.exe`)

### Setup

```bash
git clone <repository-url>
cd stream-reel-studio
pip install -r requirements.txt
```

### Configuration

Copy the example configuration file:

```bash
cp config/publisher_config.example.json config/publisher_config.json
```

Edit `config/publisher_config.json` with your credentials:
- **YouTube**: Place your OAuth `client_secrets.json` in the `config/` directory.
- **Instagram**: Add your Meta Graph API access token, Instagram User ID, and Cloudinary credentials (used as a temporary video delivery bridge).

---

## Usage

### 1. Interactive Desktop Menu (Windows)
Double-click `Publish_Reels.bat` to launch the interactive terminal menu.

### 2. Command Line Interface

```bash
# Process a video link and extract clips
python clip_master.py run --url "https://www.youtube.com/watch?v=..."

# View processed clips and approval statuses
python clip_master.py list

# Review clip details for a stream
python clip_master.py review --stream "<stream_folder_name>"

# Approve clips
python clip_master.py approve --stream "<stream_folder_name>" --clip all

# Publish approved clips
python clip_master.py post --stream "<stream_folder_name>" --clip 1 --platform all
```

---

## Using as an Antigravity Skill

This repository includes a skill definition at `.agents/skills/stream-reel-studio/SKILL.md`.

When working in Antigravity:
1. Open this workspace.
2. Provide any stream link in the prompt:
   > *"Process this link: https://youtube.com/watch?v=..., store the clips, ask for approval, and post."*
3. The assistant will invoke `clip_master.py`, present review cards, and publish upon your confirmation.
