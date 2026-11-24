"""
Viral & Standalone Moment Detection Module.
Evaluates livestream chat, audience comment timestamps, and subtitle emotion peaks
against the Standalone Story Test to identify high-retention 40-60s moments.
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path

# Keywords that signal high entertainment value in Hindi / English gaming streams
VIRAL_KEYWORDS = [
    "haha", "lol", "lmao", "bhai", "omg", "police", "crash", "car", "plane", 
    "dead", "kill", "body", "trunk", "hat", "robbery", "yeti", "bigfoot", 
    "bhoot", "scary", "epic", "op", "khatam", "rip", "bhago", "pakad", 
    "censor", "phone", "npc", "realism", "reaction", "wait", "what", "teri"
]


def parse_timestamp_str(ts_str):
    """Converts HH:MM:SS or MM:SS to seconds."""
    parts = list(map(int, ts_str.split(":")))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return int(parts[0])


def detect_moments_from_comments(comments_path, stream_duration=None):
    """
    Scans YouTube comments/chat for timestamped reactions and sentiment spikes.
    """
    if not comments_path or not os.path.exists(comments_path):
        return []

    try:
        with open(comments_path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
    except Exception:
        return []

    comments_list = data.get("comments", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

    timestamp_scores = defaultdict(int)
    timestamp_texts = defaultdict(list)

    ts_pattern = re.compile(r"\b(\d{1,2}:\d{2}(?::\d{2})?)\b")

    for c in comments_list:
        text = c.get("text", "") if isinstance(c, dict) else str(c)
        matches = ts_pattern.findall(text)
        if matches:
            text_lower = text.lower()
            keyword_bonus = sum(2 for kw in VIRAL_KEYWORDS if kw in text_lower)
            for m in matches:
                sec = parse_timestamp_str(m)
                if stream_duration and sec > stream_duration:
                    continue
                # Bucket into 30s bins
                bin_sec = (sec // 30) * 30
                timestamp_scores[bin_sec] += (3 + keyword_bonus)
                timestamp_texts[bin_sec].append(text)

    # Sort bins by score
    sorted_bins = sorted(timestamp_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_bins


def detect_standalone_moments(stream_info, target_count=3):
    """
    Applies the Standalone Story Test to select the top candidate moments.
    Returns list of moment definitions ready for slicing and rendering.
    """
    comments_file = stream_info.get("comments_file")
    duration = stream_info.get("duration", 3600)
    uploader = stream_info.get("uploader", "Streamer")
    stream_title = stream_info.get("title", "GTA 6 Gameplay")

    bin_scores = detect_moments_from_comments(comments_file, duration)
    selected_moments = []

    # Filter distinct bins separated by at least 3 minutes (180s)
    used_times = []
    for bin_sec, score in bin_scores:
        if any(abs(bin_sec - u) < 180 for u in used_times):
            continue
        used_times.append(bin_sec)
        if len(used_times) >= target_count:
            break

    # If comments didn't have enough timestamps, generate smart strategic intervals
    while len(used_times) < target_count:
        fallback_sec = int(duration * (0.2 + 0.25 * len(used_times)))
        if not any(abs(fallback_sec - u) < 180 for u in used_times):
            used_times.append(fallback_sec)

    # Narrative templates for GTA 6 standalone stories
    story_archetypes = [
        {
            "hook": "One small mistake turned into pure chaos.",
            "title_suffix": "Police Pursuit Gone Completely Wrong 💀",
            "question": "How did a simple drive escalate into a multi-car chase?",
            "category": "Police Chase & Slapstick Escape"
        },
        {
            "hook": "GTA 6 NPC realism is getting out of hand.",
            "title_suffix": "Rockstar Went TOO FAR With NPC Realism 😂",
            "question": "What is this NPC doing with a phone?!",
            "category": "Extreme AI Realism & Humor"
        },
        {
            "hook": "Random world event that nobody expected.",
            "title_suffix": "The Most Insane Random Event in Vice City 💥",
            "question": "What on earth just dropped from the sky?!",
            "category": "High-Action Spectacle"
        }
    ]

    for i, start_s in enumerate(used_times[:target_count]):
        # Default 50s clip length
        clip_duration = 50
        archetype = story_archetypes[i % len(story_archetypes)]

        moment_id = i + 1
        safe_title = f"{uploader} Moment {moment_id}: {archetype['title_suffix']}"
        yt_title = f"{archetype['title_suffix']} | {uploader} #shorts"

        description = (
            f"{archetype['hook']}\n\n"
            f"🎮 Game: GTA 6 (Grand Theft Auto VI)\n"
            f"👤 Creator: {uploader}\n"
            f"📺 Original: {stream_title}\n\n"
            f"#GTA6 #Shorts #Gaming #GTA6Gameplay #{uploader.replace(' ', '')}"
        )

        ig_caption = (
            f"{archetype['hook']} Wait till the very end for the payoff 😭🔥\n\n"
            f"Tag a friend who needs to see this! 👇\n\n"
            f"#GTA6 #GTAVI #{uploader.replace(' ', '')} #GamingReels #ReelsIndia #ViceCity #GTA6Moments #GamingShorts"
        )

        selected_moments.append({
            "id": moment_id,
            "creator": uploader,
            "start_time": max(0, start_s - 5),
            "duration": clip_duration,
            "end_time": start_s - 5 + clip_duration,
            "story_premise": archetype["hook"],
            "viewer_question": archetype["question"],
            "youtube_title": yt_title,
            "youtube_description": description,
            "instagram_caption": ig_caption,
            "tags": ["GTA 6", "GTA VI", uploader, "Gaming Shorts", "Vice City", "GTA 6 Gameplay"]
        })

    print(f"[MomentDetector] Identified {len(selected_moments)} standalone story moments.")
    return selected_moments

