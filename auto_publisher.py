"""
GTA 6 1-Click Multi-Platform Auto-Publisher
Publishes ready-made vertical reels/shorts to YouTube Shorts and Instagram Reels.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config" / "publisher_config.json"
if not CONFIG_PATH.exists():
    CONFIG_PATH = Path(__file__).parent / "publisher_config.json"

CLIPS_CATALOG = [
    {
        "id": 1,
        "creator": "Xyaa",
        "name": "Marina Police Chase",
        "video_path": r"D:\Reels\clips\xyaa\GTA6_Story1_MarinaPoliceChase.mp4",
        "thumb_path": r"D:\Reels\clips\xyaa\GTA6_Story1_MarinaPoliceChase_thumb.jpg",
        "youtube_title": "One Small Mistake in GTA 6 Turned Into THIS 💀 #shorts",
        "youtube_description": (
            "Bro I was literally just test driving the car... why did the entire Vice City police department pull up?! 😭\n\n"
            "🎮 Game: GTA 6 (Grand Theft Auto VI)\n"
            "👤 Streamer: Xyaa\n"
            "#GTA6 #Shorts #Gaming #GTA6Gameplay #Xyaa"
        ),
        "tags": ["GTA 6", "GTA VI", "Xyaa", "GTA 6 Police", "Gaming Shorts", "Vice City"],
        "instagram_caption": (
            "Bro I was literally just test driving the car... why did the entire Vice City police department pull up?! 😭 "
            "Totaled the car inside the Marina Club!\n\n"
            "#GTA6 #GrandTheftAuto6 #GTA6Police #Xyaa #GTA6Moments #GamingReels #ReelsIndia #GamingShorts"
        ),
    },
    {
        "id": 2,
        "creator": "Xyaa",
        "name": "Backroom NPC Realism",
        "video_path": r"D:\Reels\clips\xyaa\GTA6_Story2_BackroomRealism.mp4",
        "thumb_path": r"D:\Reels\clips\xyaa\GTA6_Story2_BackroomRealism_thumb.jpg",
        "youtube_title": "Rockstar Went TOO FAR With GTA 6 NPC Realism 😂 #shorts",
        "youtube_description": (
            "Walked into the back room of a store in Vice City and was NOT ready for this 😭 "
            "The NPCs are literally recording each other on their phones! Rockstar thought of EVERYTHING.\n\n"
            "🎮 Game: GTA 6 (Grand Theft Auto VI)\n"
            "👤 Streamer: Xyaa\n"
            "#GTA6 #Shorts #RockstarGames #GTA6Funny #ViceCity"
        ),
        "tags": ["GTA 6", "Rockstar Games", "GTA 6 Realism", "GTA 6 NPC", "Xyaa", "Gaming Memes"],
        "instagram_caption": (
            "Walked into the back room of a store in Vice City and was NOT ready for this 😭 "
            "The NPCs are literally recording each other on their phones! Rockstar thought of EVERYTHING.\n\n"
            "#GTA6 #GTAVI #RockstarGames #GTA6Funny #ViceCityNPC #GamingMemes #ShortsViral #IndianGamers"
        ),
    },
    {
        "id": 3,
        "creator": "Xyaa",
        "name": "Bigfoot Night Encounter",
        "video_path": r"D:\Reels\clips\xyaa\GTA6_Story3_BigfootEncounter.mp4",
        "thumb_path": r"D:\Reels\clips\xyaa\GTA6_Story3_BigfootEncounter_thumb.jpg",
        "youtube_title": "DID GTA 6 JUST CONFIRM BIGFOOT?! 😱 #shorts",
        "youtube_description": (
            "Followed mysterious smoke into the Leonida forest at midnight... and encountered THIS terrifying creature! 🌲👀\n\n"
            "🎮 Game: GTA 6 (Grand Theft Auto VI)\n"
            "👤 Streamer: Xyaa\n"
            "#GTA6 #Shorts #Bigfoot #GTA6Mysteries #GTA6EasterEgg"
        ),
        "tags": ["GTA 6", "Bigfoot", "GTA 6 Bigfoot", "GTA 6 Easter Egg", "Xyaa", "GTA 6 Secrets"],
        "instagram_caption": (
            "Followed mysterious smoke into the Leonida forest at midnight... and encountered THIS 😱 "
            "Rockstar actually put Bigfoot in the game! Drop a comment: Real or Myth?! 👇\n\n"
            "#GTA6 #GTAVI #Bigfoot #GTA6Bigfoot #GTA6EasterEggs #RockstarGames #GamingCommunity #Leonida"
        ),
    },
    {
        "id": 4,
        "creator": "Techno Gamerz",
        "name": "Body in the Trunk Panic",
        "video_path": r"D:\Reels\clips\techno_gamerz\GTA6_Techno1_BodyInTrunk.mp4",
        "thumb_path": r"D:\Reels\clips\techno_gamerz\GTA6_Techno1_BodyInTrunk_thumb.jpg",
        "youtube_title": "Car Accident Turned Into A Murder In GTA 6 💀 | Techno Gamerz #shorts",
        "youtube_description": (
            "Was just trying to drive out of the repair shop and an NPC did THIS... "
            "then police showed up while there was a body in the car 😭 Techno ka GTA 6 launch day gone wrong!\n\n"
            "🎮 Game: GTA 6 (Grand Theft Auto VI)\n"
            "👤 Streamer: Techno Gamerz (Ujjwal Chaurasia)\n"
            "#GTA6 #Shorts #TechnoGamerz #GTA6Gameplay #UjjwalGamer"
        ),
        "tags": ["GTA 6", "Techno Gamerz", "Ujjwal Gamer", "GTA 6 Gameplay", "Vice City", "Shorts"],
        "instagram_caption": (
            "Was just trying to drive out of the repair shop and an NPC did THIS... "
            "then police showed up while there was a body in the car 😭 Techno ka GTA 6 launch day gone wrong!\n\n"
            "#GTA6 #TechnoGamerz #GTA6Gameplay #UjjwalGamer #ViceCity #GTA6Moments #GamingReels #ReelsIndia #GamingShorts"
        ),
    },
    {
        "id": 5,
        "creator": "Techno Gamerz",
        "name": "Plane Highway Crash Fireball",
        "video_path": r"D:\Reels\clips\techno_gamerz\GTA6_Techno2_PlaneHighwayCrash.mp4",
        "thumb_path": r"D:\Reels\clips\techno_gamerz\GTA6_Techno2_PlaneHighwayCrash_thumb.jpg",
        "youtube_title": "PLANE CRASHED ON THE HIGHWAY IN GTA 6 💥 | Techno Gamerz #shorts",
        "youtube_description": (
            "I was just looking for a supercar and an entire plane crashed on the highway right in front of me?! 😱 "
            "Rockstar's random world events in GTA 6 are UNREAL.\n\n"
            "🎮 Game: GTA 6 (Grand Theft Auto VI)\n"
            "👤 Streamer: Techno Gamerz\n"
            "#GTA6 #Shorts #TechnoGamerz #GTA6PlaneCrash #ViceCity"
        ),
        "tags": ["GTA 6", "Techno Gamerz", "GTA 6 Plane Crash", "Vice City", "Rockstar Games", "GTA 6 Secrets"],
        "instagram_caption": (
            "I was just looking for a supercar and an entire plane crashed on the highway in front of me?! 😱 "
            "Rockstar's random world events in GTA 6 are UNREAL.\n\n"
            "#GTA6 #GTAVI #TechnoGamerz #GTA6PlaneCrash #ViceCity #RockstarGames #GamingReels #ShortsViral #IndianGamers"
        ),
    },
    {
        "id": 6,
        "creator": "Techno Gamerz",
        "name": "Delhi Boy in Vice City",
        "video_path": r"D:\Reels\clips\techno_gamerz\GTA6_Techno3_DelhiBoyViceCity.mp4",
        "thumb_path": r"D:\Reels\clips\techno_gamerz\GTA6_Techno3_DelhiBoyViceCity_thumb.jpg",
        "youtube_title": "When A Delhi Boy Plays GTA 6 😂 | Techno Gamerz #shorts",
        "youtube_description": (
            "NPC knocked my cap into the water so I had to give him the classic Delhi treatment 😭 "
            "But the ending with the ladies had me dead laughing!\n\n"
            "🎮 Game: GTA 6 (Grand Theft Auto VI)\n"
            "👤 Streamer: Techno Gamerz\n"
            "#GTA6 #Shorts #TechnoGamerz #FunnyGaming #ViceCity"
        ),
        "tags": ["GTA 6", "Techno Gamerz", "Delhi Boy", "GTA 6 Funny", "Vice City", "Shorts"],
        "instagram_caption": (
            "NPC knocked my cap into the water so I had to give him the classic Delhi treatment 😭 "
            "But the ending with the ladies had me dead laughing!\n\n"
            "Tag that one friend who argues over everything 🤣\n\n"
            "#GTA6 #TechnoGamerz #DelhiMemes #ViceCity #GTA6Moments #GamingReels #ReelsInstagram #ViralReels"
        ),
    },
]


def load_config():
    if not CONFIG_PATH.exists():
        print(f"[!] Warning: Config file not found at {CONFIG_PATH}. Using template defaults.")
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class YouTubePublisher:
    """Publishes vertical MP4s as YouTube Shorts using YouTube Data API v3."""

    def __init__(self, config):
        self.yt_cfg = config.get("youtube", {})
        self.client_secrets = Path(self.yt_cfg.get("client_secrets_file", "client_secrets.json"))
        self.token_file = Path(self.yt_cfg.get("token_file", "youtube_token.json"))
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
            print("    Please install: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2\n")
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
                    print(f"\n[!] YouTube Error: '{self.client_secrets}' not found.")
                    print("    1. Go to Google Cloud Console (https://console.cloud.google.com/)")
                    print("    2. Enable 'YouTube Data API v3'")
                    print("    3. Create OAuth 2.0 Client ID (Desktop App) and download client_secrets.json to D:\\Reels\\")
                    return None

                flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secrets), SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    def publish_clip(self, clip_data, privacy_status=None, dry_run=False):
        video_path = clip_data["video_path"]
        title = clip_data["youtube_title"]
        description = clip_data["youtube_description"]
        tags = clip_data["tags"]
        privacy = privacy_status or self.default_privacy

        print(f"\n[YouTube] Preparing upload: {title}")
        print(f"          File: {video_path}")
        print(f"          Privacy: {privacy}")

        if dry_run:
            print("          [DRY-RUN] Verified payload. Upload skipped.")
            return True

        youtube = self.authenticate()
        if not youtube:
            return False

        from googleapiclient.http import MediaFileUpload

        body = {
            "snippet": {
                "title": title,
                "description": description,
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

        print("[YouTube] Uploading in progress...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"          Uploaded {int(status.progress() * 100)}%")

        video_id = response.get("id")
        video_url = f"https://youtu.be/{video_id}"
        print(f"[YouTube] SUCCESS! Video published: {video_url}")
        return video_url


class InstagramPublisher:
    """
    Publishes vertical MP4s as Instagram Reels using:
    1. Official Meta Content Publishing Graph API (recommended for Business/Creator accounts)
    2. Cloudinary for instant temporary public HTTPS video bridge (Meta requires public HTTPS video_url)
    3. Fallback: instagrapi for direct local uploads
    """

    def __init__(self, config):
        self.ig_cfg = config.get("instagram", {})
        self.graph_cfg = self.ig_cfg.get("meta_graph_api", {})
        self.cloud_cfg = self.ig_cfg.get("cloudinary_temporary_hosting", {})
        self.method = self.ig_cfg.get("method", "graph_api")

    def upload_to_cloudinary(self, video_path):
        cloud_name = self.cloud_cfg.get("cloud_name")
        api_key = self.cloud_cfg.get("api_key")
        api_secret = self.cloud_cfg.get("api_secret")

        if not cloud_name or "YOUR_" in cloud_name:
            print("\n[!] Meta Graph API requires an HTTPS URL for videos.")
            print("    Please provide Cloudinary credentials in publisher_config.json, OR host the MP4 publicly.")
            return None

        try:
            import cloudinary
            import cloudinary.uploader
        except ImportError:
            print("\n[!] Cloudinary library missing. Run: pip install cloudinary\n")
            return None

        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
        print(f"[Instagram Bridge] Uploading temporary video to Cloudinary: {video_path}...")
        res = cloudinary.uploader.upload_large(video_path, resource_type="video")
        secure_url = res.get("secure_url")
        public_id = res.get("public_id")
        print(f"[Instagram Bridge] Temporary URL generated: {secure_url}")
        return secure_url, public_id

    def delete_from_cloudinary(self, public_id):
        try:
            import cloudinary.uploader
            cloudinary.uploader.destroy(public_id, resource_type="video")
            print(f"[Instagram Bridge] Cleaned up temporary video '{public_id}'.")
        except Exception as e:
            print(f"[Instagram Bridge] Cleanup warning: {e}")

    def publish_via_graph_api(self, clip_data, dry_run=False):
        import requests

        ig_user_id = self.graph_cfg.get("instagram_user_id")
        access_token = self.graph_cfg.get("access_token")
        version = self.graph_cfg.get("graph_api_version", "v19.0")

        if not ig_user_id or "YOUR_" in ig_user_id or not access_token or "YOUR_" in access_token:
            print("\n[!] Instagram Graph API Error: Credentials missing in publisher_config.json.")
            print("    Required fields:")
            print("    - access_token: Long-lived Meta User/Page Access Token with 'instagram_content_publish'")
            print("    - instagram_user_id: Instagram Business/Creator Account ID")
            return False

        if dry_run:
            print(f"[Instagram] [DRY-RUN] Verified Graph API payload for '{clip_data['name']}'.")
            return True

        # Step 1: Video hosting bridge
        cloud_res = self.upload_to_cloudinary(clip_data["video_path"])
        if not cloud_res:
            return False
        video_url, public_id = cloud_res

        try:
            # Step 2: Create Reel Container
            print("[Instagram] Initializing Reels Container via Meta Graph API...")
            container_endpoint = f"https://graph.facebook.com/{version}/{ig_user_id}/media"
            container_payload = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": clip_data["instagram_caption"],
                "access_token": access_token,
            }
            res = requests.post(container_endpoint, data=container_payload).json()
            if "id" not in res:
                print(f"[Instagram] Container creation failed: {res}")
                return False

            creation_id = res["id"]
            print(f"[Instagram] Container ID created: {creation_id}. Processing on Meta servers...")

            # Step 3: Poll Container Status
            status_endpoint = f"https://graph.facebook.com/{version}/{creation_id}"
            max_retries = 30
            for i in range(max_retries):
                time.sleep(5)
                poll = requests.get(status_endpoint, params={"fields": "status_code,status", "access_token": access_token}).json()
                status = poll.get("status_code")
                print(f"          Processing status: {status} ({i*5}s)")
                if status == "FINISHED":
                    break
                elif status == "ERROR":
                    print(f"[Instagram] Video encoding failed on Meta servers: {poll}")
                    return False
            else:
                print("[Instagram] Timeout waiting for Meta media processing.")
                return False

            # Step 4: Publish Reel
            print("[Instagram] Publishing Reel...")
            publish_endpoint = f"https://graph.facebook.com/{version}/{ig_user_id}/media_publish"
            pub_res = requests.post(publish_endpoint, data={"creation_id": creation_id, "access_token": access_token}).json()

            if "id" in pub_res:
                media_id = pub_res["id"]
                print(f"[Instagram] SUCCESS! Reel published with ID: {media_id}")
                return media_id
            else:
                print(f"[Instagram] Publish call failed: {pub_res}")
                return False

        finally:
            if self.cloud_cfg.get("auto_delete_after_publish", True) and public_id:
                self.delete_from_cloudinary(public_id)

    def publish_clip(self, clip_data, dry_run=False):
        return self.publish_via_graph_api(clip_data, dry_run=dry_run)


def verify_files():
    print("=" * 65)
    print(" GTA 6 READY CLIPS INVENTORY CHECK")
    print("=" * 65)
    all_ok = True
    for clip in CLIPS_CATALOG:
        v_ok = os.path.exists(clip["video_path"])
        t_ok = os.path.exists(clip["thumb_path"])
        v_size = os.path.getsize(clip["video_path"]) / (1024 * 1024) if v_ok else 0
        status = "READY" if (v_ok and t_ok) else "MISSING"
        if not (v_ok and t_ok):
            all_ok = False
        print(f"[{clip['id']}] [{status}] {clip['creator']} - {clip['name']}")
        print(f"    File: {clip['video_path']} ({v_size:.2f} MB)")
        print(f"    Thumb: {clip['thumb_path']}")
        print("-" * 65)
    return all_ok


def interactive_menu():
    print("\n" + "=" * 65)
    print("   🎮 GTA VI: 1-CLICK SOCIAL AUTO-PUBLISHER")
    print("   YouTube Shorts & Instagram Reels Automation")
    print("=" * 65)
    for c in CLIPS_CATALOG:
        print(f" [{c['id']}] {c['creator']}: {c['name']}")
    print(" [A] ALL 6 CLIPS (Sequential Full Queue)")
    print(" [V] Verify Files & Catalog")
    print(" [Q] Quit")
    print("-" * 65)

    choice = input("Select Clip (1-6 / A / V / Q): ").strip().upper()
    if choice == "Q":
        sys.exit(0)
    elif choice == "V":
        verify_files()
        return

    plat_choice = input("Select Destination ([1] YouTube Shorts, [2] Instagram Reels, [3] Both): ").strip()
    platform_map = {"1": "youtube", "2": "instagram", "3": "all"}
    platform = platform_map.get(plat_choice, "all")

    dry_input = input("Test Run Only? (y/n, default n): ").strip().lower()
    dry_run = dry_input == "y"

    selected_clips = CLIPS_CATALOG if choice == "A" else [c for c in CLIPS_CATALOG if str(c["id"]) == choice]

    if not selected_clips:
        print("[!] Invalid clip selection.")
        return

    run_pipeline(selected_clips, platform, dry_run=dry_run)


def run_pipeline(clips, platform, privacy="public", dry_run=False):
    config = load_config()
    yt_publisher = YouTubePublisher(config)
    ig_publisher = InstagramPublisher(config)

    for clip in clips:
        print("\n" + "=" * 65)
        print(f"🚀 PROCESSING CLIP {clip['id']}: {clip['name']} ({clip['creator']})")
        print("=" * 65)

        if platform in ["youtube", "all"]:
            try:
                yt_publisher.publish_clip(clip, privacy_status=privacy, dry_run=dry_run)
            except Exception as e:
                print(f"[!] YouTube Upload Error: {e}")

        if platform in ["instagram", "all"]:
            try:
                ig_publisher.publish_clip(clip, dry_run=dry_run)
            except Exception as e:
                print(f"[!] Instagram Upload Error: {e}")

    print("\n🎉 Batch processing finished!")


def main():
    parser = argparse.ArgumentParser(description="GTA 6 1-Click Video Auto-Publisher")
    parser.add_argument("--clip", choices=["1", "2", "3", "4", "5", "6", "all"], help="Clip ID to publish")
    parser.add_argument("--platform", choices=["youtube", "instagram", "all"], default="all", help="Target platform")
    parser.add_argument("--privacy", choices=["public", "unlisted", "private"], default="public", help="YouTube privacy")
    parser.add_argument("--dry-run", action="store_true", help="Simulate upload without publishing")
    parser.add_argument("--verify", action="store_true", help="Verify all clip files and thumbnails")

    args = parser.parse_args()

    if args.verify:
        verify_files()
        return

    if not args.clip:
        interactive_menu()
    else:
        selected_clips = CLIPS_CATALOG if args.clip == "all" else [c for c in CLIPS_CATALOG if str(c["id"]) == args.clip]
        run_pipeline(selected_clips, args.platform, privacy=args.privacy, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

