---
name: stream-reel-studio
description: >-
  Turn YouTube streams, podcasts, and long-form videos into viral 9:16 vertical reels and shorts
  (gaming facecam split, podcast framing, word-synced animated pop subtitles, EBU R128 audio normalization),
  manage interactive reviews/approvals, and auto-post in 1 click to YouTube Shorts and Instagram Reels.
  Use when the user shares any video link, asks to extract viral clips, batch-process streams/podcasts,
  review clips, or publish reels to social media.
---

# 🚀 Stream Reel Studio: The Creator & Faceless Channel Engine

Transform any YouTube gaming livestream, podcast, or long-form video into high-retention, monetizable **9:16 vertical Shorts and Reels** using AI agents or 1-click desktop menus.

---

## 💡 What Matters to Creators & Clipping Channels

1. **Massive Time Savings**: Turn a 4-hour livestream or 2-hour podcast into 3-5 ready-to-publish viral shorts in **60 seconds**, saving hours of manual cutting, captioning, and rendering.
2. **Algorithmic Retention (Hooks + Payoffs)**: The **Standalone Story Test** ensures every clip has an irresistible 3-second premise, escalating curiosity, and a satisfying payoff.
3. **High-Engagement Pop Subtitles**: MrBeast / Alex Hormozi style animated karaoke typography (`.ass`) with neon active-word pop and bold outlines placed safely above platform UI controls.
4. **Mastered Audio (-16 LUFS)**: EBU R128 audio normalization so dialogue is punchy, loud, and crisp on phone speakers without clipping.
5. **Passive Monetization**: Directly auto-publish to Instagram Reels and YouTube Shorts with SEO-optimized titles and 5 targeted viral hashtags.

---

## 🎬 Niche Presets

The engine supports multiple content genres via `--mode`:

- **Gaming (`--mode gaming`)**: Top 38% centered streamer facecam + bottom 62% focused gameplay. Perfect for GTA 6, Valorant, Minecraft, Call of Duty, Elden Ring, and esports streams.
- **Podcast / Talk Show (`--mode podcast`)**: Centered speaker framing with high-contrast animated dialogue typography and cinematic blurred 9:16 background. Ideal for interviews, tech talks, and philosophical discussions.
- **Auto-Detect (`--mode auto`)**: Scans video frames for facecam quadrants; if detected, applies the gaming split; otherwise applies the podcast layout.

---

## 🤖 Zero-Code Agent Setup (Antigravity, Codex, Cursor, Claude Code)

You don't need to write terminal commands. Just prompt your agent naturally:

### Single Video Prompt
> *"Clip this video: `https://www.youtube.com/watch?v=...`, give me 3 viral moments, show me preview cards, and post upon my approval."*

### Batch Processing Prompt
> *"Process these 3 podcast links in batch mode using podcast layout, generate captions, and prepare for posting."*

The agent will execute `clip_master.py`, track clip manifests, show you approval cards, and publish upon your confirmation.

---

## 💻 CLI & Developer Reference

```bash
# 1. Single Video (Cut, Auto-Subtitle & Store)
python clip_master.py run --url "<YOUTUBE_URL>" --mode auto

# 2. Batch Processing (Process a list of videos at once)
python clip_master.py batch --file batch_links.txt --mode podcast
python clip_master.py batch --urls "url1,url2,url3" --mode gaming

# 3. View All Stored Clips & Approval Statuses
python clip_master.py list

# 4. Review Generated Clips & Social Copy
python clip_master.py review --stream "<stream_slug>"

# 5. Approve Clips
python clip_master.py approve --stream "<stream_slug>" --clip all

# 6. 1-Click Publish to Social Media
python clip_master.py post --stream "<stream_slug>" --clip all --platform all
python clip_master.py post --stream "<stream_slug>" --clip 1 --platform instagram
```

---

## 🖥️ Desktop 1-Click Launcher (No Terminal Needed)

Double-click [`Publish_Reels.bat`](../../Publish_Reels.bat) to launch the interactive control panel with options to paste links, batch process, review cards, and auto-post.
