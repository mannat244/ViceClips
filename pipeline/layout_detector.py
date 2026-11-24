"""
Stream Layout & Facecam Detection Module.
Detects streamer facecam coordinates and gameplay crop areas using OpenCV.
"""

import os
import cv2
import subprocess
from pathlib import Path

FFMPEG_BIN = r"C:\ffmpeg\bin\ffmpeg.exe" if os.path.exists(r"C:\ffmpeg\bin\ffmpeg.exe") else "ffmpeg"


def extract_sample_frames(video_slice_path, out_dir, count=3):
    """Extracts a few sample frames from a sliced video."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = []

    cap = cv2.VideoCapture(str(video_slice_path))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        total_frames = 100

    step = max(1, total_frames // (count + 1))
    for i in range(1, count + 1):
        target_f = step * i
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_f)
        ret, frame = cap.read()
        if ret:
            fpath = out_dir / f"sample_{i}.jpg"
            cv2.imwrite(str(fpath), frame)
            frames.append(str(fpath))
    cap.release()
    return frames


def detect_layout(sample_video_or_frames, known_preset=None):
    """
    Detects streamer webcam coordinates and stream dimensions.
    Returns layout dictionary:
    {
       "has_facecam": True/False,
       "facecam_crop": "x:y:w:h",
       "gameplay_crop": "x:y:w:h",
       "width": int,
       "height": int
    }
    """
    if known_preset:
        return known_preset

    # Load Haar cascade
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Determine frames
    if isinstance(sample_video_or_frames, list):
        frame_paths = sample_video_or_frames
    else:
        temp_frames_dir = Path(sample_video_or_frames).parent / "temp_detect_frames"
        frame_paths = extract_sample_frames(sample_video_or_frames, temp_frames_dir)

    if not frame_paths:
        # Default fallback
        return {
            "has_facecam": False,
            "facecam_crop": None,
            "gameplay_crop": "crop=1200:1080:360:0",
            "width": 1920,
            "height": 1080
        }

    first_img = cv2.imread(frame_paths[0])
    h, w = first_img.shape[:2]

    # Check common streamer facecam zones:
    # 1. Top-Right: x ~ 1400..1920, y ~ 0..500
    # 2. Mid-Right: x ~ 1450..1920, y ~ 350..850
    # 3. Bottom-Right: x ~ 1400..1920, y ~ 600..1080
    # 4. Top-Left: x ~ 0..500, y ~ 0..500
    # 5. Bottom-Left: x ~ 0..500, y ~ 600..1080

    candidate_zones = [
        {"name": "top_right", "box": (int(w * 0.72), 30, int(w * 0.25), int(h * 0.45)), "cam_crop": f"crop={int(w*0.23)}:{int(h*0.42)}:{int(w*0.75)}:40"},
        {"name": "mid_right", "box": (int(w * 0.75), int(h * 0.35), int(w * 0.23), int(h * 0.45)), "cam_crop": f"crop=440:440:1480:400"},
        {"name": "bottom_right", "box": (int(w * 0.72), int(h * 0.55), int(w * 0.25), int(h * 0.42)), "cam_crop": f"crop={int(w*0.23)}:{int(h*0.4)}:{int(w*0.75)}:{int(h*0.58)}"},
        {"name": "top_left", "box": (20, 20, int(w * 0.25), int(h * 0.42)), "cam_crop": f"crop={int(w*0.23)}:{int(h*0.4)}:30:30"},
        {"name": "bottom_left", "box": (20, int(h * 0.55), int(w * 0.25), int(h * 0.42)), "cam_crop": f"crop={int(w*0.23)}:{int(h*0.4)}:30:{int(h*0.58)}"}
    ]

    best_zone = None
    max_face_detections = 0

    for zone in candidate_zones:
        zx, zy, zw, zh = zone["box"]
        hits = 0
        for fpath in frame_paths:
            img = cv2.imread(fpath)
            if img is None:
                continue
            crop = img[zy:zy+zh, zx:zx+zw]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(40, 40))
            if len(faces) > 0:
                hits += 1
        if hits > max_face_detections:
            max_face_detections = hits
            best_zone = zone

    has_cam = max_face_detections >= 1
    facecam_crop = best_zone["cam_crop"] if has_cam else None

    # Gameplay crop logic: center 1200x(min(h, 1080))
    gameplay_w = min(1200, w)
    gameplay_x = max(0, (w - gameplay_w) // 2)
    gameplay_crop = f"crop={gameplay_w}:{h}:{gameplay_x}:0"

    layout_config = {
        "has_facecam": has_cam,
        "facecam_crop": facecam_crop,
        "gameplay_crop": gameplay_crop,
        "detected_zone": best_zone["name"] if best_zone else None,
        "width": w,
        "height": h
    }
    print(f"[LayoutDetector] Stream layout analyzed: has_facecam={has_cam}, zone={layout_config['detected_zone']}, dims={w}x{h}")
    return layout_config

