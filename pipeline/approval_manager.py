"""
Approval Manager & Storage Registry Module.
Stores rendered clips, manages manifest states (pending_approval, approved, rejected, posted),
and generates approval review reports.
"""

import os
import json
from pathlib import Path


def init_stream_manifest(stream_dir, stream_info, clips_data):
    """Initializes manifest.json in the stream's clip folder."""
    stream_path = Path(stream_dir)
    stream_path.mkdir(parents=True, exist_ok=True)
    manifest_path = stream_path / "manifest.json"

    clips_records = []
    for c in clips_data:
        clips_records.append({
            "id": c["id"],
            "title": c.get("story_premise", f"Clip {c['id']}"),
            "youtube_title": c.get("youtube_title"),
            "youtube_description": c.get("youtube_description"),
            "instagram_caption": c.get("instagram_caption"),
            "tags": c.get("tags", []),
            "start_time": c.get("start_time"),
            "duration": c.get("duration"),
            "video_file": str(c.get("video_file")),
            "thumb_file": str(c.get("thumb_file")),
            "status": "pending_approval",  # pending_approval, approved, rejected, posted
            "published_urls": {}
        })

    manifest = {
        "stream_id": stream_info.get("id"),
        "stream_title": stream_info.get("title"),
        "uploader": stream_info.get("uploader"),
        "total_duration": stream_info.get("duration"),
        "created_at": None,
        "clips": clips_records
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[ApprovalManager] Initialized stream manifest: {manifest_path}")
    return manifest


def load_manifest(stream_dir):
    """Loads manifest.json from stream directory."""
    manifest_path = Path(stream_dir) / "manifest.json"
    if not manifest_path.exists():
        return None
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(stream_dir, manifest):
    """Saves updated manifest.json."""
    manifest_path = Path(stream_dir) / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def set_clip_approval(stream_dir, clip_id, status="approved", notes=None):
    """Updates status for a specific clip in manifest."""
    manifest = load_manifest(stream_dir)
    if not manifest:
        raise FileNotFoundError(f"Manifest not found in {stream_dir}")

    found = False
    for c in manifest.get("clips", []):
        if str(c["id"]) == str(clip_id):
            c["status"] = status
            if notes:
                c["notes"] = notes
            found = True
            break

    if found:
        save_manifest(stream_dir, manifest)
        print(f"[ApprovalManager] Clip {clip_id} status updated to: '{status}'")
        return True
    return False


def set_clip_published(stream_dir, clip_id, platform, live_url):
    """Marks a clip as published with its live social media URL."""
    manifest = load_manifest(stream_dir)
    if not manifest:
        return False

    for c in manifest.get("clips", []):
        if str(c["id"]) == str(clip_id):
            c["status"] = "posted"
            c["published_urls"][platform] = live_url
            break

    save_manifest(stream_dir, manifest)
    return True


def generate_review_markdown(stream_dir):
    """Generates a clean Markdown review card for the user."""
    manifest = load_manifest(stream_dir)
    if not manifest:
        return "Manifest not found."

    md = []
    md.append(f"# 🎬 Review & Approval: {manifest['uploader']} - {manifest['stream_title']}")
    md.append(f"**Stream ID**: `{manifest['stream_id']}` | **Clips Count**: {len(manifest['clips'])}\n")
    md.append("---\n")

    for c in manifest["clips"]:
        status_emoji = "⏳ PENDING APPROVAL" if c["status"] == "pending_approval" else ("✅ APPROVED" if c["status"] == "approved" else "🚀 POSTED")
        md.append(f"### Clip {c['id']}: {c['title']} ({status_emoji})")
        md.append(f"- **Video Path**: [`{Path(c['video_file']).name}`](file:///{c['video_file'].replace('\\', '/')})")
        md.append(f"- **Thumbnail**: [`{Path(c['thumb_file']).name}`](file:///{c['thumb_file'].replace('\\', '/')})")
        md.append(f"- **Shorts Title**: `{c['youtube_title']}`")
        md.append(f"- **Instagram Caption**:\n  > {c['instagram_caption']}\n")
        md.append(f"- **Commands to Approve / Post**:")
        md.append(f"  - Approve: `python clip_master.py approve --stream \"{Path(stream_dir).name}\" --clip {c['id']}`")
        md.append(f"  - Post: `python clip_master.py post --stream \"{Path(stream_dir).name}\" --clip {c['id']} --platform all`\n")
        md.append("---\n")

    return "\n".join(md)

