"""
🎮 GTA VI & Stream Clipper Master Orchestrator (clip_master.py)

Unified end-to-end pipeline CLI:
  1. Process (Cut & Store): Ingest link, detect viral moments, crop layout, render 9:16 vertical reels.
  2. Review & Approve: Review video previews, titles, and social copy.
  3. Post: 1-click publishing to YouTube Shorts and Instagram Reels.

Usage:
  python clip_master.py run --url "https://www.youtube.com/watch?v=..."
  python clip_master.py list
  python clip_master.py review --stream <slug>
  python clip_master.py approve --stream <slug> --clip <id_or_all>
  python clip_master.py post --stream <slug> --clip <id_or_all> --platform [youtube|instagram|all]
"""

import os
import sys
import re
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from pipeline.downloader import get_stream_metadata, slice_stream
from pipeline.layout_detector import detect_layout
from pipeline.moment_detector import detect_standalone_moments
from pipeline.subtitle_styler import generate_ass_subtitles
from pipeline.reel_renderer import render_vertical_reel
from pipeline.approval_manager import (
    init_stream_manifest,
    load_manifest,
    set_clip_approval,
    set_clip_published,
    generate_review_markdown,
)
from pipeline.publisher import load_publisher_config, YouTubePublisher, InstagramPublisher


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "_", text)[:40]


def process_stream_pipeline(url, target_moments=3, mode="auto"):
    print("\n" + "=" * 70)
    print(f"🎬 PROCESSING STREAM: {url} (Mode: {mode})")
    print("=" * 70)

    # Step 1: Ingest & Metadata
    temp_dir = BASE_DIR / "temp" / f"stream_{int(os.getpid())}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    stream_info = get_stream_metadata(url, temp_dir)
    stream_title = stream_info.get("title", "Livestream")
    uploader = stream_info.get("uploader", "Streamer")
    stream_slug = f"{slugify(uploader)}_{slugify(stream_title)}"

    # Dedicated output directory under clips/
    stream_clips_dir = BASE_DIR / "clips" / stream_slug
    stream_clips_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[Pipeline] Stream: {stream_title} by {uploader}")
    print(f"[Pipeline] Output Destination: {stream_clips_dir}")

    # Step 2: Detect Viral Moments
    print("\n" + "-" * 70)
    print("🔍 STAGE 2: Standalone Story & Moment Detection")
    print("-" * 70)
    moments = detect_standalone_moments(stream_info, target_count=target_moments)

    # Step 3: Layout Detection (Extract a small 10s slice to analyze layout)
    print("\n" + "-" * 70)
    print("📐 STAGE 3: Stream Layout & Facecam Analysis")
    print("-" * 70)
    sample_slice_path = temp_dir / "sample_probe.mp4"
    probe_start = moments[0]["start_time"] if moments else 120
    slice_stream(stream_info["direct_urls"], probe_start, 10, sample_slice_path)
    layout_cfg = detect_layout(str(sample_slice_path))

    # Step 4: Slicing, Subtitling, and Rendering
    rendered_clips = []
    for m in moments:
        m_id = m["id"]
        print("\n" + "-" * 70)
        print(f"✂️ STAGE 4.{m_id}: Slicing & Rendering Clip {m_id} ({m['duration']}s)")
        print(f"   Hook: {m['story_premise']}")
        print("-" * 70)

        raw_slice = temp_dir / f"raw_slice_{m_id}.mp4"
        ass_path = temp_dir / f"subs_{m_id}.ass"
        out_mp4 = stream_clips_dir / f"clip_{m_id}.mp4"
        out_thumb = stream_clips_dir / f"clip_{m_id}_thumb.jpg"

        # 4a. Slice stream
        slice_stream(stream_info["direct_urls"], m["start_time"], m["duration"], raw_slice)

        # 4b. Subtitles
        generate_ass_subtitles(stream_info.get("subs_file"), m["start_time"], m["duration"], ass_path)

        # 4c. Render Vertical Reel
        render_vertical_reel(raw_slice, ass_path, layout_cfg, out_mp4, out_thumb, mode=mode)

        m["video_file"] = str(out_mp4)
        m["thumb_file"] = str(out_thumb)
        rendered_clips.append(m)

    # Step 5: Initialize Manifest & Save
    manifest = init_stream_manifest(stream_clips_dir, stream_info, rendered_clips)

    # Step 6: Presentation / Approval Report
    print("\n" + "=" * 70)
    print("✅ CUTS STORED SUCCESSFULLY! READY FOR REVIEW & APPROVAL")
    print("=" * 70)
    report = generate_review_markdown(stream_clips_dir)
    print(report)

    print("\n👉 To Approve & Post:")
    print(f"   python clip_master.py approve --stream \"{stream_slug}\" --clip all")
    print(f"   python clip_master.py post --stream \"{stream_slug}\" --clip all --platform all")
    return stream_slug


def process_batch_pipeline(urls, target_moments=3, mode="auto"):
    print("\n" + "=" * 70)
    print(f"🚀 LAUNCHING BATCH PROCESSING FOR {len(urls)} STREAMS/VIDEOS")
    print("=" * 70)
    completed_slugs = []
    for idx, u in enumerate(urls, 1):
        clean_url = u.strip()
        if not clean_url or clean_url.startswith("#"):
            continue
        print(f"\n[{idx}/{len(urls)}] Processing batch item: {clean_url}")
        try:
            slug = process_stream_pipeline(clean_url, target_moments=target_moments, mode=mode)
            completed_slugs.append(slug)
        except Exception as e:
            print(f"[!] Error processing batch item '{clean_url}': {e}")

    print("\n" + "=" * 70)
    print(f"🎉 BATCH COMPLETE: Successfully processed {len(completed_slugs)} of {len(urls)} videos!")
    print("=" * 70)
    for s in completed_slugs:
        print(f"  • {s}")
    return completed_slugs


def list_all_streams():
    clips_dir = BASE_DIR / "clips"
    print("\n" + "=" * 70)
    print(" 📂 REGISTERED STREAM CLIPS IN WORKSPACE")
    print("=" * 70)

    found = False
    for sub in clips_dir.iterdir():
        if sub.is_dir() and sub.name != "drafts":
            manifest = load_manifest(sub)
            if manifest:
                found = True
                print(f"\n📁 Stream: {sub.name}")
                print(f"   Channel: {manifest.get('uploader')} | Title: {manifest.get('stream_title')}")
                for c in manifest.get("clips", []):
                    st = c.get("status", "unknown").upper()
                    print(f"   - [Clip {c['id']}] [{st}] {c['title']}")
                    print(f"     Video: {c['video_file']}")
            else:
                # Check for mp4s directly
                mp4s = list(sub.glob("*.mp4"))
                if mp4s:
                    found = True
                    print(f"\n📁 Folder: {sub.name} ({len(mp4s)} videos)")
                    for v in mp4s:
                        print(f"   - {v.name}")

    if not found:
        print("No processed streams found yet.")
    print("\n" + "=" * 70)


def approve_stream_clips(stream_name, clip_arg):
    stream_dir = BASE_DIR / "clips" / stream_name
    manifest = load_manifest(stream_dir)
    if not manifest:
        print(f"[!] Stream manifest not found in: {stream_dir}")
        return

    if clip_arg.lower() == "all":
        for c in manifest.get("clips", []):
            set_clip_approval(stream_dir, c["id"], status="approved")
        print(f"\n🎉 All clips in '{stream_name}' have been APPROVED!")
    else:
        set_clip_approval(stream_dir, clip_arg, status="approved")
        print(f"\n🎉 Clip {clip_arg} in '{stream_name}' has been APPROVED!")


def post_stream_clips(stream_name, clip_arg, platform="all", privacy="public", dry_run=False):
    stream_dir = BASE_DIR / "clips" / stream_name
    manifest = load_manifest(stream_dir)
    if not manifest:
        print(f"[!] Stream manifest not found in: {stream_dir}")
        return

    config = load_publisher_config()
    yt_publisher = YouTubePublisher(config)
    ig_publisher = InstagramPublisher(config)

    clips_to_post = manifest.get("clips", [])
    if clip_arg.lower() != "all":
        clips_to_post = [c for c in clips_to_post if str(c["id"]) == str(clip_arg)]

    for c in clips_to_post:
        print("\n" + "=" * 70)
        print(f"🚀 PUBLISHING CLIP {c['id']}: {c['title']}")
        print(f"   Current Status: {c['status']}")
        print("=" * 70)

        if c["status"] != "approved" and not dry_run:
            print(f"[!] Warning: Clip {c['id']} is currently '{c['status']}' (not approved).")
            confirm = input("    Publish anyway? (y/n): ").strip().lower()
            if confirm != "y":
                print("    Skipping.")
                continue

        # YouTube Shorts
        if platform in ["youtube", "all"]:
            try:
                yt_url = yt_publisher.publish(c, privacy=privacy, dry_run=dry_run)
                if yt_url:
                    set_clip_published(stream_dir, c["id"], "youtube", yt_url)
            except Exception as e:
                print(f"[!] YouTube Publish Error: {e}")

        # Instagram Reels
        if platform in ["instagram", "all"]:
            try:
                ig_url = ig_publisher.publish(c, dry_run=dry_run)
                if ig_url:
                    set_clip_published(stream_dir, c["id"], "instagram", ig_url)
            except Exception as e:
                print(f"[!] Instagram Publish Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="GTA 6 & Gaming Stream Reels Master Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # Command: run (cut & store)
    run_parser = subparsers.add_parser("run", help="Full automated pipeline: download, cut, format, and store")
    run_parser.add_argument("--url", required=True, help="YouTube video or stream URL")
    run_parser.add_argument("--count", type=int, default=3, help="Number of moments to extract")
    run_parser.add_argument("--mode", choices=["auto", "gaming", "podcast", "generic"], default="auto", help="Content layout mode")

    # Command: batch (multi-video / multi-link)
    batch_parser = subparsers.add_parser("batch", help="Batch process multiple YouTube streams, podcasts, or links")
    batch_parser.add_argument("--file", help="Path to text file containing YouTube URLs (one per line)")
    batch_parser.add_argument("--urls", help="Comma-separated list of YouTube URLs")
    batch_parser.add_argument("--count", type=int, default=3, help="Number of moments per video")
    batch_parser.add_argument("--mode", choices=["auto", "gaming", "podcast", "generic"], default="auto", help="Content layout mode")

    # Command: list
    subparsers.add_parser("list", help="List all processed streams and clips")

    # Command: review
    rev_parser = subparsers.add_parser("review", help="Review clips and approval report for a stream")
    rev_parser.add_argument("--stream", required=True, help="Stream folder name (slug)")

    # Command: approve
    app_parser = subparsers.add_parser("approve", help="Approve clip for posting")
    app_parser.add_argument("--stream", required=True, help="Stream folder name (slug)")
    app_parser.add_argument("--clip", required=True, help="Clip ID (1, 2, 3...) or 'all'")

    # Command: post
    post_parser = subparsers.add_parser("post", help="Publish approved clips to social media")
    post_parser.add_argument("--stream", required=True, help="Stream folder name (slug)")
    post_parser.add_argument("--clip", required=True, help="Clip ID or 'all'")
    post_parser.add_argument("--platform", choices=["youtube", "instagram", "all"], default="all")
    post_parser.add_argument("--privacy", choices=["public", "unlisted", "private"], default="public")
    post_parser.add_argument("--dry-run", action="store_true", help="Simulate upload without publishing")

    args = parser.parse_args()

    if args.command == "run":
        process_stream_pipeline(args.url, target_moments=args.count, mode=args.mode)
    elif args.command == "batch":
        urls_to_process = []
        if args.file:
            p = Path(args.file)
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    urls_to_process.extend([line.strip() for line in f if line.strip() and not line.strip().startswith("#")])
            else:
                print(f"[!] Batch file not found: {args.file}")
                return
        if args.urls:
            urls_to_process.extend([u.strip() for u in args.urls.split(",") if u.strip()])
        if not urls_to_process:
            print("[!] No URLs provided. Use --file <path> or --urls \"<url1>,<url2>\"")
            return
        process_batch_pipeline(urls_to_process, target_moments=args.count, mode=args.mode)
    elif args.command == "list":
        list_all_streams()
    elif args.command == "review":
        stream_dir = BASE_DIR / "clips" / args.stream
        print(generate_review_markdown(stream_dir))
    elif args.command == "approve":
        approve_stream_clips(args.stream, args.clip)
    elif args.command == "post":
        post_stream_clips(args.stream, args.clip, platform=args.platform, privacy=args.privacy, dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

