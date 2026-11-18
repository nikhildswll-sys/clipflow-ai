import os
import sys
import json
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CloudAutoPilot")

def main():
    logger.info("Starting Cloud AutoPilot Job...")

    # 1. Restore credentials from GitHub Secrets if present
    base_dir = os.path.dirname(os.path.abspath(__file__))
    token_file = os.path.join(base_dir, "youtube_token.json")
    secret_file = os.path.join(base_dir, "client_secret.json")

    env_token = os.environ.get("YOUTUBE_TOKEN")
    env_secret = os.environ.get("CLIENT_SECRET")

    if env_token and not os.path.exists(token_file):
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(env_token)
        logger.info("Restored youtube_token.json from environment secret.")

    if env_secret and not os.path.exists(secret_file):
        with open(secret_file, "w", encoding="utf-8") as f:
            f.write(env_secret)
        logger.info("Restored client_secret.json from environment secret.")

    if not os.path.exists(token_file):
        logger.error("No YouTube token available. Run local authentication first!")
        sys.exit(1)

    # 2. Pick current viral topic based on hourly slot
    from autopilot import AutoPilotService
    service = AutoPilotService()
    
    # Select topic by current hour / minute hash
    slot = int(time.time() // 1800) # 30 min slots
    topic_item = service.topics[slot % len(service.topics)]
    query = topic_item["topic"]
    hook = topic_item.get("hook", "WAIT FOR IT... 🤯")
    category = topic_item.get("category", "Trending")

    logger.info(f"Slot {slot}: Selected Topic: '{query}' ({category})")

    # 3. Search YouTube for top video
    search_cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "--dump-json",
        "--no-playlist"
    ]
    res = subprocess.run(search_cmd, stdout=subprocess.PIPE, text=True)
    if res.returncode != 0 or not res.stdout.strip():
        logger.error(f"Search failed for {query}")
        sys.exit(1)

    video_info = json.loads(res.stdout.strip().splitlines()[0])
    yt_url = video_info.get("webpage_url") or video_info.get("url")
    title = video_info.get("title", query)
    logger.info(f"Target video found: {title} ({yt_url})")

    # 4. Download first 70s segment
    os.makedirs(os.path.join(base_dir, "storage", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "storage", "exports"), exist_ok=True)
    raw_video = os.path.join(base_dir, "storage", "uploads", f"cloud_{int(time.time())}.mp4")

    dl_cmd = [
        "yt-dlp",
        "-f", "bv*[height<=720]+ba/b[height<=720]/b",
        "--download-sections", "*00:00:15-00:01:00",
        "--merge-output-format", "mp4",
        "-o", raw_video,
        yt_url
    ]
    subprocess.run(dl_cmd, check=True)
    logger.info(f"Downloaded video segment: {raw_video}")

    # 5. Render 9:16 vertical Short
    rendered_video = os.path.join(base_dir, "storage", "exports", f"short_{int(time.time())}.mp4")
    render_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-vf", "crop=ih*(9/16):ih,scale=1080:1920:flags=lanczos,drawtext=text='" + hook.replace("'", "") + "':x=(w-text_w)/2:y=180:fontsize=48:fontcolor=white:box=1:boxcolor=red@0.9:boxborderw=18",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        rendered_video
    ]
    subprocess.run(render_cmd, check=True)
    logger.info(f"Rendered 9:16 Short: {rendered_video}")

    # 6. Upload to YouTube Shorts
    from youtube_uploader import YouTubeUploader
    upload_res = YouTubeUploader.upload_short(
        video_path=rendered_video,
        title=f"{hook} {category} #Shorts",
        description=f"{query}\n\nAuto-curated by ClipFlow AI.\n#Shorts #Viral #Gaming #GTA6 #{category.replace(' ', '')}",
        tags=["#Shorts", "#GTA6", "#Gaming", "#Viral", "#Trending"],
        privacy_status="public",
        client_secrets_path=secret_file
    )

    logger.info(f"Upload Result: {upload_res}")
    print("FINISHED_SUCCESSFULLY:", upload_res.get("video_url"))

if __name__ == "__main__":
    main()
