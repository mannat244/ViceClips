---
name: stream-reel-studio
description: >-
  Automated gaming livestream and video clipping, vertical 9:16 reel formatting
  (streamer facecam split, word-synced animated subtitles, EBU R128 audio normalization),
  review/approval management, and 1-click social publishing to YouTube Shorts and Instagram Reels.
  Use when the user shares a YouTube stream/video link to cut, asks to extract viral moments,
  review generated clips, or publish reels to Instagram and YouTube Shorts.
---

# 🎮 Stream Reel Studio: Automated Clipping & Social Publishing

This skill provides an end-to-end automated pipeline to transform multi-hour gaming livestreams and long-form videos into high-retention, broadcast-quality **9:16 vertical reels and shorts**, manage approval workflows, and publish them with a single click to **Instagram Reels** and **YouTube Shorts**.

---

## 📋 The 4-Stage Workflow

```
[Link Input] ──> [1. Cut & Format] ──> [2. Store] ──> [3. Take Approval] ──> [4. 1-Click Post]
```

1. **Ingest & Detect**: Extract metadata, chat reactions, and auto-subtitles. Apply the **Standalone Story Test** to discover the 3 best self-contained moments (40–60s each).
2. **Cut & Format**: Fast-seek HLS slicing via FFmpeg (takes ~15s without downloading the full stream). Split layout into top facecam (38%) and bottom gameplay (62%). Overlay word-synced animated `.ass` karaoke subtitles and normalize audio to `-16 LUFS`.
3. **Store**: Save high-definition video, cover thumbnail, catchy Shorts title, and Instagram caption with 5 targeted hashtags into `clips/<stream_slug>/manifest.json`.
4. **Take Approval**: Generate an interactive review card in chat or CLI with preview links. Pause for user approval (`approved` status).
5. **Post**: Publish approved clips to **Instagram Reels** (via Meta Content Publishing API + Cloudinary bridge) and **YouTube Shorts** (via YouTube Data API v3).

---

## 🛠️ CLI Quick Reference

The master CLI is located at [`clip_master.py`](../../clip_master.py) in the project root:

```bash
# 1. Process any YouTube stream/video (Cut, format, and store)
python clip_master.py run --url "<YOUTUBE_URL>" --count 3

# 2. List all registered streams and their approval statuses
python clip_master.py list

# 3. View review report & copy for a specific stream
python clip_master.py review --stream "<STREAM_SLUG>"

# 4. Approve clips for posting
python clip_master.py approve --stream "<STREAM_SLUG>" --clip all
python clip_master.py approve --stream "<STREAM_SLUG>" --clip 1

# 5. 1-Click Post approved clips to social media
python clip_master.py post --stream "<STREAM_SLUG>" --clip 1 --platform all
python clip_master.py post --stream "<STREAM_SLUG>" --clip 1 --platform instagram
python clip_master.py post --stream "<STREAM_SLUG>" --clip 1 --platform youtube

# 6. Test dry-run without uploading
python clip_master.py post --stream "<STREAM_SLUG>" --clip 1 --platform all --dry-run
```

---

## 🎯 Standalone Story Test Standards

Every selected clip must function as an independent, scroll-stopping story. Always enforce:

1. **Premise Hook (0–5s)**: A clear question or bizarre incident that makes the viewer ask *"Why is this happening?"* or *"What is going to happen next?"*.
2. **Setup & Escalation (5–35s)**: Rising tension, chaos, or comedic dialogue that keeps retention high.
3. **Payoff (35–50s)**: An unexpected twist, punchline, disaster, or reaction that rewards the viewer for staying.
4. **Reject Weak Footage**:
   - ❌ Ordinary driving without an incident.
   - ❌ Generic shooting without narrative context.
   - ❌ Streamer laughing at chat when the in-game cause is not visible.

---

## 📐 Video Specifications

- **Format**: MP4 (H.264 / AAC)
- **Dimensions**: `1080 × 1920` (9:16 Vertical)
- **Framerate**: `60 FPS`
- **Layout**: Top 38% (Streamer Facecam centered) + Bottom 62% (Centered Gameplay)
- **Subtitles**: Styled ASS with thick black borders and neon active-word pop highlights placed safely above social media UI buttons (`MarginV=680`).
- **Audio Target**: EBU R128 loudness normalization (`loudnorm=I=-16:TP=-1.5:LRA=11`).

---

## ⚙️ Configuration File (`config/publisher_config.json`)

To enable social media publishing, populate [`config/publisher_config.json`](../../config/publisher_config.json):

```json
{
  "youtube": {
    "enabled": true,
    "client_secrets_file": "config/client_secrets.json",
    "token_file": "config/youtube_token.json",
    "default_privacy": "public",
    "category_id": "20"
  },
  "instagram": {
    "enabled": true,
    "method": "graph_api",
    "meta_graph_api": {
      "access_token": "YOUR_META_ACCESS_TOKEN",
      "instagram_user_id": "YOUR_INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "graph_api_version": "v19.0"
    },
    "cloudinary_temporary_hosting": {
      "enabled": true,
      "cloud_name": "YOUR_CLOUDINARY_CLOUD_NAME",
      "api_key": "YOUR_CLOUDINARY_API_KEY",
      "api_secret": "YOUR_CLOUDINARY_API_SECRET",
      "auto_delete_after_publish": true
    }
  }
}
```

---

## 💡 Troubleshooting & Validation

- **Verify configuration and clips**:
  ```bash
  python auto_publisher.py --verify
  ```
- **Windows 1-Click GUI/Menu**:
  Double-click [`Publish_Reels.bat`](../../Publish_Reels.bat) for an interactive menu with zero terminal typing.
