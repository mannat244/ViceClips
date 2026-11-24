"""
Interactive API Key Setup & Diagnostic Wizard.
Guides users step-by-step through configuring Meta Graph API, Cloudinary, and YouTube Data API,
verifies credentials live, and saves config/publisher_config.json.
"""

import os
import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
CONFIG_DIR = BASE_DIR / "config"
CONFIG_PATH = CONFIG_DIR / "publisher_config.json"
EXAMPLE_CONFIG_PATH = CONFIG_DIR / "publisher_config.example.json"


def load_existing_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    if EXAMPLE_CONFIG_PATH.exists():
        with open(EXAMPLE_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print(f"\n✅ Configuration saved to: {CONFIG_PATH}")


def test_cloudinary(cloud_name, api_key, api_secret):
    try:
        import cloudinary
        import cloudinary.api
        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
        usage = cloudinary.api.usage()
        print(f"   [Cloudinary] Connection Verified! Plan: {usage.get('plan')}")
        return True
    except Exception as e:
        print(f"   [Cloudinary] Verification Warning: {e}")
        return False


def test_instagram(token, ig_user_id):
    try:
        url = f"https://graph.facebook.com/v19.0/{ig_user_id}"
        res = requests.get(url, params={"fields": "id,username,name", "access_token": token}).json()
        if "username" in res:
            print(f"   [Instagram] Connection Verified! Connected as @{res['username']} ({res.get('name')})")
            return True
        elif "error" in res:
            print(f"   [Instagram] Verification Warning: {res['error'].get('message')}")
            return False
    except Exception as e:
        print(f"   [Instagram] Error checking account: {e}")
        return False


def run_setup_wizard():
    print("\n" + "=" * 70)
    print(" 🧙‍♂️ STREAM REEL STUDIO: INTERACTIVE API & CREDENTIALS SETUP WIZARD")
    print("=" * 70)
    print("This wizard will gently guide you through connecting Instagram Reels,")
    print("YouTube Shorts, and the Cloudinary video bridge in under 3 minutes.\n")

    cfg = load_existing_config()
    ig_cfg = cfg.setdefault("instagram", {})
    meta_cfg = ig_cfg.setdefault("meta_graph_api", {})
    cloud_cfg = ig_cfg.setdefault("cloudinary_temporary_hosting", {})
    yt_cfg = cfg.setdefault("youtube", {})

    # ---------------------------------------------------------
    # 1. Cloudinary Setup (Video delivery bridge for Meta)
    # ---------------------------------------------------------
    print("─" * 70)
    print("☁️ STEP 1: Cloudinary Video Bridge (Free Tier: 25GB/month)")
    print("─" * 70)
    print("Meta's API requires a secure public link to ingest your vertical videos.")
    print("Cloudinary hosts the video temporarily, sends it to Instagram, and the script")
    print("automatically deletes it right after publishing.\n")
    print("👉 Get your free keys at: https://cloudinary.com/users/register_free")
    print("   (Dashboard -> Product Environment Credentials -> Cloud Name, API Key, API Secret)\n")

    curr_cname = cloud_cfg.get("cloud_name", "")
    curr_key = cloud_cfg.get("api_key", "")
    curr_sec = cloud_cfg.get("api_secret", "")

    cname_prompt = f"Cloud Name [{curr_cname}]: " if curr_cname and "YOUR_" not in curr_cname else "Cloud Name: "
    val_cname = input(cname_prompt).strip()
    if val_cname:
        cloud_cfg["cloud_name"] = val_cname

    key_prompt = f"API Key [{curr_key}]: " if curr_key and "YOUR_" not in curr_key else "API Key: "
    val_key = input(key_prompt).strip()
    if val_key:
        cloud_cfg["api_key"] = val_key

    sec_prompt = f"API Secret [{curr_sec[:6]}...]: " if curr_sec and "YOUR_" not in curr_sec else "API Secret: "
    val_sec = input(sec_prompt).strip()
    if val_sec:
        cloud_cfg["api_secret"] = val_sec

    cloud_cfg["enabled"] = True
    cloud_cfg["auto_delete_after_publish"] = True

    if cloud_cfg.get("cloud_name") and "YOUR_" not in cloud_cfg["cloud_name"]:
        print("\nVerifying Cloudinary connection...")
        test_cloudinary(cloud_cfg["cloud_name"], cloud_cfg["api_key"], cloud_cfg["api_secret"])

    # ---------------------------------------------------------
    # 2. Instagram Reels (Meta Graph API)
    # ---------------------------------------------------------
    print("\n" + "─" * 70)
    print("📸 STEP 2: Instagram Reels (Meta Graph API)")
    print("─" * 70)
    print("Publishes vertical reels with custom captions and 5 viral hashtags directly to your profile.\n")
    print("Requirements:")
    print("1. Instagram Professional (Creator or Business) Account")
    print("2. Meta Developer App: https://developers.facebook.com/")
    print("3. Generate User Token: https://developers.facebook.com/tools/explorer/")
    print("   (Permission required: 'instagram_content_publish')\n")

    curr_ig_id = meta_cfg.get("instagram_user_id", "")
    curr_token = meta_cfg.get("access_token", "")

    id_prompt = f"Instagram Business Account ID [{curr_ig_id}]: " if curr_ig_id and "YOUR_" not in curr_ig_id else "Instagram Business Account ID: "
    val_id = input(id_prompt).strip()
    if val_id:
        meta_cfg["instagram_user_id"] = val_id

    tok_prompt = f"Meta Access Token [{curr_token[:10]}...]: " if curr_token and "YOUR_" not in curr_token else "Meta Access Token: "
    val_tok = input(tok_prompt).strip()
    if val_tok:
        meta_cfg["access_token"] = val_tok

    meta_cfg["graph_api_version"] = "v19.0"
    ig_cfg["enabled"] = True

    if meta_cfg.get("access_token") and meta_cfg.get("instagram_user_id"):
        print("\nVerifying Instagram connection...")
        test_instagram(meta_cfg["access_token"], meta_cfg["instagram_user_id"])

    # ---------------------------------------------------------
    # 3. YouTube Shorts (Google Cloud Data API v3)
    # ---------------------------------------------------------
    print("\n" + "─" * 70)
    print("🔴 STEP 3: YouTube Shorts (Google Cloud OAuth)")
    print("─" * 70)
    print("Uploads 9:16 videos directly from your hard drive with #Shorts tags.\n")
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Enable 'YouTube Data API v3'")
    print("3. Create OAuth 2.0 Client ID (Desktop App) and download client_secrets.json")
    print(f"4. Place client_secrets.json in: {CONFIG_DIR}\\client_secrets.json\n")

    client_secrets_path = CONFIG_DIR / "client_secrets.json"
    if client_secrets_path.exists():
        print("   ✅ Found config/client_secrets.json! YouTube API is ready.")
        yt_cfg["client_secrets_file"] = "config/client_secrets.json"
        yt_cfg["enabled"] = True
    else:
        print("   ⏳ config/client_secrets.json not found yet (you can add this anytime).")
        yt_cfg["client_secrets_file"] = "config/client_secrets.json"

    # Save
    save_config(cfg)

    print("\n" + "=" * 70)
    print("🎉 SETUP COMPLETE!")
    print("=" * 70)
    print("You can test your setup at any time with:")
    print("  python clip_master.py list")
    print("  python Publish_Reels.bat")
    print("=" * 70)


if __name__ == "__main__":
    run_setup_wizard()
