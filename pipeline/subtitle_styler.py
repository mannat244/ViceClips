"""
Subtitle & Typography Styler Module.
Converts WebVTT auto-captions into animated word-synced ASS (Advanced SubStation Alpha)
karaoke subtitles optimized for mobile retention on 9:16 vertical video.
"""

import re
from pathlib import Path


def parse_vtt_timestamp(ts):
    """Converts HH:MM:SS.mmm or MM:SS.mmm to seconds float."""
    ts = ts.strip()
    parts = ts.split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return float(parts[0])


def format_ass_timestamp(seconds):
    """Formats float seconds into H:MM:SS.cc for ASS script."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def generate_ass_subtitles(vtt_file_path, clip_start_sec, clip_duration_sec, out_ass_path):
    """
    Parses VTT, extracts cues in the clip interval, groups words into punchy 3-5 word lines,
    and writes out a high-retention .ass subtitle file with animated pop styling.
    """
    out_ass_path = Path(out_ass_path)
    out_ass_path.parent.mkdir(parents=True, exist_ok=True)

    clip_end_sec = clip_start_sec + clip_duration_sec

    # Read VTT file
    lines = []
    if vtt_file_path and Path(vtt_file_path).exists():
        with open(vtt_file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

    cue_pattern = re.compile(r"(\d{1,2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})")
    word_pattern = re.compile(r"<(\d{1,2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})><c>(.*?)</c>")

    events = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = cue_pattern.match(line)
        if m:
            c_start = parse_vtt_timestamp(m.group(1))
            c_end = parse_vtt_timestamp(m.group(2))

            text_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and not cue_pattern.match(lines[i]):
                text_lines.append(lines[i].strip())
                i += 1

            full_text = " ".join(text_lines)

            # Check if cue overlaps with our clip window
            if c_end >= clip_start_sec and c_start <= clip_end_sec:
                # Relative time to clip start
                rel_start = max(0.0, c_start - clip_start_sec)
                rel_end = min(clip_duration_sec, c_end - clip_start_sec)

                # Extract word-level tags if present
                sub_words = word_pattern.findall(full_text)
                if sub_words:
                    # Parse internal words
                    first_word = re.split(r"<", full_text)[0].strip()
                    word_list = []
                    if first_word:
                        word_list.append((rel_start, first_word))
                    for w_ts, w_txt in sub_words:
                        w_rel = parse_vtt_timestamp(w_ts) - clip_start_sec
                        clean_w = re.sub(r"<.*?>", "", w_txt).strip()
                        if clean_w:
                            word_list.append((max(0.0, w_rel), clean_w))

                    if word_list:
                        events.append({
                            "start": rel_start,
                            "end": rel_end,
                            "words": word_list
                        })
                else:
                    # Plain line without word tags
                    clean_text = re.sub(r"<.*?>", "", full_text).strip()
                    if clean_text:
                        events.append({
                            "start": rel_start,
                            "end": rel_end,
                            "plain": clean_text
                        })
        else:
            i += 1

    # Build ASS Content with MrBeast / Hormozi styling
    ass_header = """[Script Info]
Title: Standalone Story Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,64,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5.5,2.5,2,80,80,680,1
Style: Highlight,Impact,68,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,105,105,1,0,1,6.0,3.0,2,80,80,680,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    ass_events = []
    # If no subtitles were parsed, produce empty valid ASS file
    if not events:
        with open(out_ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header)
        return str(out_ass_path)

    for ev in events:
        start_fmt = format_ass_timestamp(ev["start"])
        end_fmt = format_ass_timestamp(ev["end"])

        if "words" in ev and ev["words"]:
            words = ev["words"]
            # Break words into chunks of 4 for maximum readability
            chunk_size = 4
            for c_idx in range(0, len(words), chunk_size):
                chunk = words[c_idx:c_idx + chunk_size]
                chunk_start = chunk[0][0]
                chunk_end = words[min(c_idx + chunk_size, len(words) - 1)][0] + 0.8
                chunk_end = min(ev["end"], chunk_end)

                c_start_fmt = format_ass_timestamp(chunk_start)
                c_end_fmt = format_ass_timestamp(chunk_end)

                # Format chunk with active word pop
                chunk_words = [w[1] for w in chunk]
                line_text = " ".join(chunk_words).upper()

                # Highlight the first or most dramatic word in neon yellow
                styled_line = f"{{\\c&H0000FFFF&}}{chunk_words[0].upper()}{{\\c&H00FFFFFF&}} " + " ".join(chunk_words[1:]).upper()
                ass_events.append(f"Dialogue: 0,{c_start_fmt},{c_end_fmt},Default,,0,0,0,,{styled_line}")
        elif "plain" in ev and ev["plain"]:
            plain_text = ev["plain"].upper()
            # Split long sentences into 4-word bites
            tokens = plain_text.split()
            if len(tokens) > 5:
                half = len(tokens) // 2
                t_mid = ev["start"] + (ev["end"] - ev["start"]) / 2
                l1 = " ".join(tokens[:half])
                l2 = " ".join(tokens[half:])
                ass_events.append(f"Dialogue: 0,{start_fmt},{format_ass_timestamp(t_mid)},Default,,0,0,0,,{l1}")
                ass_events.append(f"Dialogue: 0,{format_ass_timestamp(t_mid)},{end_fmt},Default,,0,0,0,,{l2}")
            else:
                ass_events.append(f"Dialogue: 0,{start_fmt},{end_fmt},Default,,0,0,0,,{plain_text}")

    full_ass = ass_header + "\n".join(ass_events) + "\n"
    with open(out_ass_path, "w", encoding="utf-8") as f:
        f.write(full_ass)

    print(f"[SubtitleStyler] Generated styled ASS subtitles with {len(ass_events)} lines: {out_ass_path.name}")
    return str(out_ass_path)

