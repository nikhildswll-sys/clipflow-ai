import os
import sys
import time
import datetime
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BatchScheduler")

def run_batch_schedule(count: int = 6, interval_minutes: int = 30):
    """
    Renders multiple viral 9:16 Shorts at once on your laptop
    and schedules their publishing on YouTube at 30-minute intervals!
    Once uploaded, you can TURN OFF your laptop, and YouTube will
    automatically release each Short every 30 minutes!
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    token_file = os.path.join(base_dir, "youtube_token.json")
    secret_file = os.path.join(base_dir, "client_secret.json")

    if not os.path.exists(token_file):
        logger.error("youtube_token.json not found! Please run python authenticate_youtube.py first.")
        sys.exit(1)

    from autopilot import AutoPilotService
    from main import import_youtube_video, StreamRequest, render_clip, RenderClipRequest, PROJECTS_DB
    from youtube_uploader import YouTubeUploader
    import subprocess, json

    service = AutoPilotService()
    topics = service.topics[:count]

    logger.info("=" * 65)
    logger.info(f"🚀 BATCH SHORTS SCHEDULER: Generating & Scheduling {len(topics)} Shorts")
    logger.info(f"Interval: Every {interval_minutes} minutes | Once finished, LAPTOP CAN BE SHUT DOWN!")
    logger.info("=" * 65)

    now = datetime.datetime.now(datetime.timezone.utc)
    scheduled_results = []

    for idx, t in enumerate(topics):
        query = t["topic"]
        hook = t["hook"]
        category = t["category"]

        # Calculate exact future release time for this Short
        release_time = now + datetime.timedelta(minutes=(idx + 1) * interval_minutes)
        publish_at_iso = release_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        logger.info(f"\n[{idx+1}/{len(topics)}] Processing: '{query}'")
        logger.info(f"📅 Scheduled Release: {release_time.strftime('%Y-%m-%d %H:%M:%S UTC')} (in {(idx+1)*interval_minutes} mins)")

        # 1. Search YouTube locally (Residential IP - zero bot checks)
        search_cmd = ["yt-dlp", f"ytsearch1:{query}", "--dump-json", "--no-playlist"]
        try:
            res = subprocess.run(search_cmd, stdout=subprocess.PIPE, text=True, timeout=30)
            if res.returncode != 0 or not res.stdout.strip():
                logger.warning(f"Could not find video for {query}, skipping...")
                continue
            video_info = json.loads(res.stdout.strip().splitlines()[0])
            yt_url = video_info.get("webpage_url") or video_info.get("url")
            title = video_info.get("title", query)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            continue

        # 2. Ingest and transcribe
        logger.info(f"Ingesting: {title}...")
        try:
            req = StreamRequest(stream_url=yt_url, auto_generate=True)
            proj = import_youtube_video(req)
            proj_id = proj["id"]

            full_proj = PROJECTS_DB.get(proj_id, {})
            clips = full_proj.get("clips", [])
            if not clips:
                logger.warning(f"No viral moments found in {title}, skipping...")
                continue

            best_clip = clips[0]

            # 3. Render 9:16 vertical with Hormozi Clean captions & bottom position
            logger.info("Rendering 9:16 Short with Hormozi Clean captions...")
            render_req = RenderClipRequest(
                project_id=proj_id,
                clip_id=best_clip["id"],
                aspect_ratio="9:16",
                resolution="1080p",
                caption_style="hormozi",
                custom_captions={
                    "position": "bottom",
                    "box_style": "none",
                    "font_size": "medium",
                    "fontname": "Anton",
                    "highlight_color": "#FFDE00",
                    "has_emojis": True,
                    "uppercase": True
                }
            )
            render_res = render_clip(render_req)
            video_path = render_res.get("file_path")

            if not video_path or not os.path.exists(video_path):
                logger.error(f"Render failed for clip {best_clip['id']}")
                continue

            # 4. Upload to YouTube as SCHEDULED PUBLISH
            logger.info(f"Uploading to YouTube with Scheduled Release at {publish_at_iso}...")
            upload_title = f"{hook} {category} #Shorts"
            upload_res = YouTubeUploader.upload_short(
                video_path=video_path,
                title=upload_title[:95],
                description=f"{query}\n\nAuto-curated by ClipFlow AI.\n#Shorts #GTA6 #Gaming #Viral #{category.replace(' ', '')}",
                tags=["#Shorts", "#GTA6", "#Gaming", "#Viral", "#Trending"],
                privacy_status="private", # YouTube requires private when scheduling
                client_secrets_path=secret_file,
                publish_at=publish_at_iso
            )

            if upload_res.get("status") == "success":
                logger.info(f"✅ SUCCESSFULLY SCHEDULED: {upload_res.get('video_url')} (Goes public at {publish_at_iso})")
                scheduled_results.append({
                    "title": upload_title,
                    "url": upload_res.get("video_url"),
                    "publish_at": publish_at_iso
                })
            else:
                logger.error(f"Upload failed: {upload_res.get('message')}")

        except Exception as e:
            logger.error(f"Error processing {query}: {e}")

    logger.info("\n" + "=" * 65)
    logger.info(f"🎉 BATCH COMPLETE! {len(scheduled_results)}/{len(topics)} Shorts Scheduled on YouTube!")
    logger.info("You can now safely SHUT DOWN your laptop!")
    logger.info("YouTube's servers will automatically release each Short every 30 minutes!")
    logger.info("=" * 65)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    run_batch_schedule(count=count, interval_minutes=interval)
