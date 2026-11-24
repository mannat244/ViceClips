# 🔥 Stream Reel Studio (ViralClip Engine)

> **Turn Any YouTube Livestream, Podcast, or Long-Form Video into Viral 9:16 Shorts & Reels in 60 Seconds — Cut, Format, Auto-Subtitle, Review, & Auto-Post to Earn Big.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Agent Compatible](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Codex%20%7C%20Claude%20%7C%20Cursor-purple)](https://antigravity.google)
[![YouTube Shorts](https://img.shields.io/badge/YouTube-Shorts%20API%20v3-red?logo=youtube)](https://developers.google.com/youtube/v3)
[![Instagram Reels](https://img.shields.io/badge/Instagram-Reels%20API-E4405F?logo=instagram)](https://developers.facebook.com/)
[![Zero-Code](https://img.shields.io/badge/Setup-Zero--Code%20Friendly-success)]()

---

## 💰 Why Creators & Faceless Channels Use This to Earn Big

Short-form content on YouTube Shorts and Instagram Reels is the fastest way to build an audience, secure brand sponsorships, and generate passive monetization. But manually watching hours of footage, trimming timestamps, cropping aspect ratios, and transcribing word-by-word subtitles takes 3–5 hours per video.

**Stream Reel Studio automates the entire production line:**

| What Matters | Manual Editing (Old Way) | Stream Reel Studio (Our Way) |
| :--- | :--- | :--- |
| **Time per Clip** | 1 to 2 hours of scrubbing & keyframing | **60 seconds (HLS stream seek in seconds)** |
| **Viral Curation** | Guessing timestamps randomly | **Audience reaction clustering & Standalone Story Test** |
| **Subtitle Styling** | Manual text layer transcription in Premiere/CapCut | **Word-synced animated pop typography (Hormozi/MrBeast style)** |
| **Mobile Aspect Ratio** | Tedious manual pan & scan cropping | **Automatic Facecam top (38%) + Gameplay bottom (62%) split** |
| **Audio Loudness** | Inconsistent audio that clips or sounds quiet | **EBU R128 broadcast normalization (-16 LUFS)** |
| **Publishing** | Downloading to phone, re-uploading, re-typing copy | **1-Click automated API push to Instagram & YouTube Shorts** |

---

## 🎬 Built for Every Content Niche

Whether you run a dedicated clipping channel or create original content:

- 🎮 **GTA 6 & Gaming Livestreams (`--mode gaming`)**:
  Automatically separates streamer webcam into top 38% and centers gameplay in bottom 62%. Detects high-energy screams, police chases, chaotic crashes, and funny fails.
- 🎙️ **Podcasts & Talk Shows (`--mode podcast`)**:
  Aesthetic blurred 9:16 background with focused center speaker framing and high-contrast dialogue captions. Perfect for interviews, motivation channels, and philosophical clips.
- 🎭 **IRL, Comedy & Reaction Streams (`--mode generic`)**:
  Detects laughter spikes in chat, sudden visual twists, and punchlines.
- 📈 **Faceless Clipping Channels (`batch` mode)**:
  Queue up 5 to 10 stream URLs before going to bed. Wake up to a library of rendered, captioned, ready-to-post clips.

---

## 🚀 3 Ways to Use (Zero-Code to Developer CLI)

### 1. 🤖 Zero-Code with AI Agents (Antigravity, Codex, Cursor, Claude Code)
You don't even need to open a terminal! Just open this project in your AI agent and type:

> *"Here is the stream link: `https://youtube.com/watch?v=...`. Extract 3 viral moments, show me review cards, and post to Instagram upon my approval."*

The agent loads the built-in [`.agents/skills/stream-reel-studio/SKILL.md`](.agents/skills/stream-reel-studio/SKILL.md), runs the pipeline, shows you the video preview cards with captions, and publishes on your command.

---

### 2. 🖱️ Zero-Code Windows Desktop Launcher (1-Click)
Double-click [`Publish_Reels.bat`](Publish_Reels.bat) on your desktop for an interactive menu:

```text
==============================================================================
      🔥 STREAM REEL STUDIO: CUT, AUTO-SUBTITLE, APPROVE & POST
      Transform Gaming Streams, Podcasts & Videos into Viral Shorts & Reels
==============================================================================
  [1] Cut Single Video / Stream (Enter URL - Gaming, Podcast, or IRL)
  [2] Batch Process Multiple Links (Process a list of videos at once)
  [3] Review & Approve Pending Clips (Review titles, captions & status)
  [4] 1-Click Publish Approved Clips (Push to Instagram Reels & Shorts)
  [5] Quick Direct Publisher Menu
  [6] List All Registered Clips & Analytics
  [Q] Quit
==============================================================================
```

---

### 3. ⚡ Power-User Command Line (CLI)

```bash
# 1. Single Stream Processing (Cut, Format, Subtitle & Store)
python clip_master.py run --url "https://www.youtube.com/watch?v=169ZzvPxvvM" --mode gaming

# 2. Podcast Processing
python clip_master.py run --url "https://www.youtube.com/watch?v=PODCAST_ID" --mode podcast

# 3. Batch Processing (Process 10 videos from a text file)
python clip_master.py batch --file batch_links.txt --mode auto

# 4. View All Stored Clips & Approval States
python clip_master.py list

# 5. Review Clip Details & Copy
python clip_master.py review --stream "techno_gamerz"

# 6. Approve Clips
python clip_master.py approve --stream "techno_gamerz" --clip all

# 7. 1-Click Post Approved Clips to Social Media
python clip_master.py post --stream "techno_gamerz" --clip all --platform all
```

---

## 📐 The Standalone Story Test: Why These Clips Retain Viewers

A visually impressive clip that lacks context gets scrolled past. Every moment extracted by this engine must pass the **Standalone Story Test**:

1. **The 3-Second Hook**: An intriguing premise (*"Why is this happening?"* or *"One mistake turned into a police pursuit"*).
2. **Setup & Escalation**: Fast-paced dialogue or rising danger with active word-pop captions keeping eyes glued to the center screen.
3. **Unexpected Payoff**: A punchline, spectacular explosion, sudden death, or streamer reaction that makes viewers comment and share.

---

## ⚡ Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
git clone https://github.com/your-username/stream-reel-studio.git
cd stream-reel-studio
pip install -r requirements.txt
```

*(Ensure [FFmpeg](https://ffmpeg.org/download.html) is installed and available on your system path).*

### 2. Configure Credentials
Copy the example config:
```bash
copy config\publisher_config.example.json config\publisher_config.json
```

Add your keys to `config/publisher_config.json`:
- **Instagram Reels**: Add your Meta Graph API `access_token`, `instagram_user_id`, and free [Cloudinary](https://cloudinary.com/) keys (used as a temporary bridge for Meta's servers to fetch the video).
- **YouTube Shorts**: Place your Google Cloud OAuth `client_secrets.json` into `config/`.

---

## 📂 Repository Structure

```
.
├── .agents/skills/stream-reel-studio/   # Antigravity & AI Agent Skill runbook
├── config/                             # Configuration templates (git-ignored secrets)
│   └── publisher_config.example.json
├── pipeline/                           # Modular core engine
│   ├── downloader.py                   # HLS high-speed stream slicing & metadata extraction
│   ├── layout_detector.py              # OpenCV facecam detector & safe crop bounds
│   ├── moment_detector.py              # Standalone Story Test highlight discovery
│   ├── subtitle_styler.py              # Hormozi/MrBeast word-synced ASS karaoke styling
│   ├── reel_renderer.py                # 1080x1920 60FPS vertical compositor + -16 LUFS audio
│   ├── approval_manager.py             # Manifest tracking & review reports
│   └── publisher.py                    # Multi-platform upload engines (Instagram + YouTube)
├── clips/                              # Structured output folders & manifests
├── batch_links.example.txt             # Example queue file for batch slicing
├── clip_master.py                      # Master CLI orchestrator
├── auto_publisher.py                   # Direct publisher script
├── Publish_Reels.bat                   # Windows interactive 1-click launcher
├── pyproject.toml                      # Modern packaging specification
└── requirements.txt                    # Python dependencies
```

---

## 📄 License

Distributed under the [MIT License](LICENSE). Build, customize, and monetize freely!
