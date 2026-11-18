import os
import json
import logging
from typing import Dict, Any, Optional

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
except ImportError:
    pass

logger = logging.getLogger("YouTubeUploader")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

class YouTubeUploader:
    """
    Automated YouTube Shorts Uploader using official YouTube Data API v3.
    Supports title, description, #Shorts tags, privacy status, and scheduling.
    """

    @classmethod
    def get_authenticated_service(cls, client_secrets_file: str, token_file: str = "token.json"):
        """
        Authenticates user with OAuth2 and caches credentials in token.json
        """
        creds = None
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            except Exception as e:
                logger.warning(f"Error loading cached credentials: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_file, "w", encoding="utf-8") as token:
                token.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    @classmethod
    def upload_short(
        cls,
        video_path: str,
        title: str,
        description: str,
        tags: list = None,
        privacy_status: str = "public", # 'public', 'private', or 'unlisted'
        client_secrets_path: Optional[str] = None,
        publish_at: Optional[str] = None # ISO 8601 format e.g. "2026-11-18T10:30:00Z" for Scheduled Publishing
    ) -> Dict[str, Any]:
        """
        Uploads a rendered 9:16 video as a YouTube Short.
        Supports YouTube Scheduled Publishing (publishAt) so videos go live automatically
        even when user's PC is turned off!
        """
        if not os.path.exists(video_path):
            return {"status": "error", "message": f"Video file not found: {video_path}"}

        # Auto-ensure #Shorts tag in title/tags for algorithm categorization
        if "#Shorts" not in title and "#shorts" not in title:
            title = f"{title} #Shorts"

        tags = tags or ["#Shorts", "#Viral", "#Trending"]

        secrets_file = client_secrets_path or os.path.join(os.path.dirname(__file__), "client_secret.json")
        if not os.path.exists(secrets_file):
            return {
                "status": "error",
                "message": f"YouTube client_secret.json not found at {secrets_file}. Please place your OAuth2 client secret file there."
            }

        token_file = os.path.join(os.path.dirname(__file__), "youtube_token.json")

        try:
            youtube = cls.get_authenticated_service(secrets_file, token_file)

            status_dict = {
                "selfDeclaredMadeForKids": False
            }

            if publish_at:
                # When scheduling in advance, YouTube requires privacyStatus to be "private"
                status_dict["privacyStatus"] = "private"
                status_dict["publishAt"] = publish_at
            else:
                status_dict["privacyStatus"] = privacy_status

            body = {
                "snippet": {
                    "title": title[:100],
                    "description": f"{description}\n\n#Shorts #ViralShorts",
                    "tags": tags,
                    "categoryId": "22" # People & Blogs or Entertainment
                },
                "status": status_dict
            }

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
            req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

            logger.info(f"Uploading '{title}' to YouTube...")
            response = req.execute()
            video_id = response.get("id")
            video_url = f"https://youtube.com/shorts/{video_id}"
            logger.info(f"Successfully uploaded YouTube Short: {video_url}")

            return {
                "status": "success",
                "video_id": video_id,
                "video_url": video_url,
                "privacy_status": privacy_status
            }
        except Exception as e:
            logger.error(f"YouTube upload failed: {e}")
            return {"status": "error", "message": str(e)}
