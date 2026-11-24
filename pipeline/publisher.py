"""
Social Publisher Engine Module.
Publishes approved vertical clips directly to YouTube Shorts and Instagram Reels via APIs.
"""

import os
import sys
import json
import time
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "publisher_config.json"


def load_publisher_config(config_path=None):
    cfg_file = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not cfg_file.exists():
        # Fallback to root if moved
        root_cfg = Path(__file__).parent.parent / "publisher_config.json"
        if root_cfg.exists():
            cfg_file = root_cfg
        else:
            return {}
    with open(cfg_file, "r", encoding="utf-8") as f:
        return json.load(f)


class YouTubePublisher:
    """Uploads vertical MP4s directly from disk as YouTube Shorts."""

    def __init__(self, config):
        self.yt_cfg = config.get("youtube", {})
        self.client_secrets = Path(self.yt_cfg.get("client_secrets_file", "config/client_secrets.json"))
        if not self.client_secrets.exists():
            self.client_secrets = Path(__file__).parent.parent / "client_secrets.json"
        self.token_file = Path(self.yt_cfg.get("token_file", "config/youtube_token.json"))
        if not self.token_file.exists():
            self.token_file = Path(__file__).parent.parent / "youtube_token.json"
        self.category_id = self.yt_cfg.get("category_id", "20")
        self.default_privacy = self.yt_cfg.get("default_privacy", "public")

    def authenticate(self):
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
        except ImportError:
            print("\n[!] Missing Google API libraries.")
            print("    Run: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2\n")
            return None

        SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
        creds = None

        if self.token_file.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.client_secrets.exists():
                    print(f"\n[!] YouTube Error: client_secrets.json not found.")
                    print("    Download OAuth 2.0 Desktop credentials from Google Cloud Console to D:\\Reels\\config\\client_secrets.json")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secrets), SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    def publish(self, clip_record, privacy="public", dry_run=False):
        video_path = clip_record["video_file"]
        title = clip_record["youtube_title"]
        desc = clip_record["youtube_description"]
        tags = clip_record.get("tags", ["Shorts", "GTA 6"])

        print(f"\n[YouTube Publisher] Preparing: {title}")
        print(f"                    Video: {video_path}")
        print(f"                    Privacy: {privacy}")

        if dry_run:
            print("                    [DRY-RUN] Verified payload. Upload skipped.")
            return "https://youtu.be/DRY_RUN_ID"

        youtube = self.authenticate()
        if not youtube:
            return None

        from googleapiclient.http import MediaFileUpload

        body = {
            "snippet": {
                "title": title,
                "description": desc,
                "tags": tags,
                "categoryId": self.category_id,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(video_path, chunksize=1024 * 1024 * 5, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        print("[YouTube Publisher] Upload in progress...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"                    Progress: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        yt_url = f"https://youtu.be/{video_id}"
        print(f"[YouTube Publisher] SUCCESS! Live URL: {yt_url}")
        return yt_url


class InstagramPublisher:
    """Publishes vertical MP4s as Instagram Reels using Meta Content Publishing API."""

    def __init__(self, config):
        self.ig_cfg = config.get("instagram", {})
        self.graph_cfg = self.ig_cfg.get("meta_graph_api", {})
        self.cloud_cfg = self.ig_cfg.get("cloudinary_temporary_hosting", {})

    def upload_to_cloudinary(self, video_path):
        cloud_name = self.cloud_cfg.get("cloud_name")
        api_key = self.cloud_cfg.get("api_key")
        api_secret = self.cloud_cfg.get("api_secret")

        if not cloud_name or "YOUR_" in cloud_name:
            print("\n[!] Instagram Reels API requires an HTTPS URL.")
            print("    Set your free Cloudinary credentials in publisher_config.json.\n")
            return None

        try:
            import cloudinary
            import cloudinary.uploader
        except ImportError:
            print("\n[!] Cloudinary library missing. Run: pip install cloudinary\n")
            return None

        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
        print(f"[Instagram Bridge] Staging temporary video on Cloudinary...")
        res = cloudinary.uploader.upload_large(video_path, resource_type="video")
        return res.get("secure_url"), res.get("public_id")

    def publish(self, clip_record, dry_run=False):
        import requests

        ig_user_id = self.graph_cfg.get("instagram_user_id")
        access_token = self.graph_cfg.get("access_token")
        version = self.graph_cfg.get("graph_api_version", "v19.0")

        if not ig_user_id or "YOUR_" in ig_user_id or not access_token or "YOUR_" in access_token:
            print("\n[!] Instagram Error: Meta Graph API credentials missing in publisher_config.json.")
            return None

        if dry_run:
            print(f"[Instagram Publisher] [DRY-RUN] Verified Reels payload for '{clip_record['title']}'.")
            return "https://instagram.com/reel/DRY_RUN_ID"

        cloud_res = self.upload_to_cloudinary(clip_record["video_file"])
        if not cloud_res:
            return None
        video_url, public_id = cloud_res

        try:
            # Create Reel Container
            print("[Instagram Publisher] Creating Reels Container...")
            container_url = f"https://graph.facebook.com/{version}/{ig_user_id}/media"
            payload = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": clip_record["instagram_caption"],
                "access_token": access_token
            }
            res = requests.post(container_url, data=payload).json()
            if "id" not in res:
                print(f"[Instagram Publisher] Container error: {res}")
                return None

            creation_id = res["id"]
            print(f"[Instagram Publisher] Container ID: {creation_id}. Waiting for Meta encoding...")

            # Poll Status
            status_url = f"https://graph.facebook.com/{version}/{creation_id}"
            for i in range(30):
                time.sleep(5)
                poll = requests.get(status_url, params={"fields": "status_code", "access_token": access_token}).json()
                status = poll.get("status_code")
                print(f"                      Status: {status} ({i*5}s)")
                if status == "FINISHED":
                    break
                elif status == "ERROR":
                    print(f"[Instagram Publisher] Processing failed on Meta servers: {poll}")
                    return None
            else:
                print("[Instagram Publisher] Timeout waiting for Meta media processing.")
                return None

            # Publish
            print("[Instagram Publisher] Publishing Reel live...")
            pub_url = f"https://graph.facebook.com/{version}/{ig_user_id}/media_publish"
            pub_res = requests.post(pub_url, data={"creation_id": creation_id, "access_token": access_token}).json()
            if "id" in pub_res:
                media_id = pub_res["id"]
                ig_reel_url = f"https://instagram.com/reel/{media_id}"
                print(f"[Instagram Publisher] SUCCESS! Reel ID: {media_id}")
                return ig_reel_url
            else:
                print(f"[Instagram Publisher] Publish call failed: {pub_res}")
                return None
        finally:
            if public_id and self.cloud_cfg.get("auto_delete_after_publish", True):
                try:
                    import cloudinary.uploader
                    cloudinary.uploader.destroy(public_id, resource_type="video")
                    print(f"[Instagram Bridge] Cleaned up temporary cloud video.")
                except Exception:
                    pass

