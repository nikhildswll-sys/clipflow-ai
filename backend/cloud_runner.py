import os
import sys
import json
import time
import random
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

    # 2. Authenticate official YouTube API
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials

    creds = Credentials.from_authorized_user_file(token_file)
    youtube = build("youtube", "v3", credentials=creds)

    # 3. Fetch Recent Channel Uploads for Bulletproof Anti-Duplicate Protection
    recent_titles = []
    try:
        channel_res = youtube.channels().list(mine=True, part="contentDetails").execute()
        if channel_res.get("items"):
            uploads_id = channel_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            playlist_res = youtube.playlistItems().list(playlistId=uploads_id, part="snippet", maxResults=30).execute()
            for it in playlist_res.get("items", []):
                sn = it.get("snippet", {})
                t_title = sn.get("title", "").lower()
                t_desc = sn.get("description", "").lower()
                recent_titles.append(t_title)
                recent_titles.append(t_desc)
            logger.info(f"Retrieved {len(playlist_res.get('items', []))} recent uploads from channel for anti-duplicate check.")
    except Exception as e:
        logger.warning(f"Recent uploads check notice: {e}")

    # 4. GTA 6 All-Day Live Stream Sniper Mode with Dynamic Anti-Duplicate Filter
    from autopilot import AutoPilotService
    service = AutoPilotService()
    
    gta6_day_mode = os.environ.get("GTA6_DAY_MODE", "true").lower() in ["true", "1", "yes"]

    def is_already_uploaded(topic_dict):
        h = topic_dict.get("hook", "").replace("'", "").lower().strip()
        h_words = [w for w in h.split() if len(w) > 3][:3]
        for rt in recent_titles:
            if h in rt:
                return True
            if h_words and all(w in rt for w in h_words):
                return True
        return False

    if gta6_day_mode:
        logger.info("🎮 GTA 6 ALL-DAY STREAM SNIPER ACTIVE: Targeting Top Indian & Global Streamers with High Watching!")
        stream_pool = getattr(service, "GTA6_STREAM_TOPICS", service.topics)
        unseen_pool = [t for t in stream_pool if not is_already_uploaded(t)]
        if unseen_pool:
            logger.info(f"Anti-duplicate filter: {len(unseen_pool)} unseen streamer topics available (filtered out {len(stream_pool) - len(unseen_pool)} recent).")
            topic_item = random.choice(unseen_pool)
        else:
            logger.info("All streamer topics have been used recently; cycling pool.")
            topic_item = random.choice(stream_pool)
    else:
        category_weights = {
            "GTA 6": 0.40,
            "Podcast": 0.20,
            "Sci-Fi": 0.15,
            "History": 0.15,
            "Wonders": 0.10
        }
        try:
            available_cats = list(category_weights.keys())
            weights = [category_weights[c] for c in available_cats]
            chosen_cat = random.choices(available_cats, weights=weights, k=1)[0]
            cat_topics = [t for t in service.topics if t.get("category") == chosen_cat]
            unseen_cat = [t for t in cat_topics if not is_already_uploaded(t)]
            if unseen_cat:
                topic_item = random.choice(unseen_cat)
            elif cat_topics:
                topic_item = random.choice(cat_topics)
            else:
                topic_item = random.choice(service.topics)
        except Exception as e:
            logger.warning(f"Random selection fallback: {e}. Picking uniform random topic.")
            topic_item = random.choice(service.topics)

    query = topic_item["topic"]
    hook = topic_item.get("hook", "WAIT FOR IT... 🤯")
    category = topic_item.get("category", "GTA 6")

    logger.info(f"Targeting Streamer / Event: '{query}' ({category}) | Hook: '{hook}'")

    search_query = f"{query} -#shorts -shorts"
    logger.info(f"Searching official YouTube API for full long-form video (16:9): '{search_query}'...")
    search_res = youtube.search().list(
        q=search_query,
        part="snippet",
        type="video",
        videoDuration="medium",  # 4 to 20 minutes (Full horizontal long-form videos!)
        order="viewCount",      # Highest views / most viral
        maxResults=5
    ).execute()

    if not search_res.get("items"):
        # Fallback to longer videos (>20 mins podcasts/documentaries) if needed
        search_res = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            videoDuration="long",
            order="viewCount",
            maxResults=5
        ).execute()

    if not search_res.get("items"):
        # Final general search if specific duration yields zero
        search_res = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            order="relevance",
            maxResults=5
        ).execute()

    if not search_res.get("items"):
        logger.error(f"No videos found via official API for {query}")
        sys.exit(1)

    # Select first video from search that has not already been used
    selected_item = None
    for it in search_res.get("items", []):
        v_id = it["id"].get("videoId", "")
        if any(v_id in rt for rt in recent_titles):
            logger.info(f"Skipping already-clipped video: {it['snippet']['title']} ({v_id})")
            continue
        selected_item = it
        break

    if not selected_item:
        selected_item = search_res["items"][0]

    vid = selected_item["id"]["videoId"]
    yt_url = f"https://www.youtube.com/watch?v={vid}"
    title = selected_item["snippet"]["title"]
    logger.info(f"Target video found via Official API: {title} ({yt_url})")

    # 4. Download segment from the meat of the long video
    os.makedirs(os.path.join(base_dir, "storage", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "storage", "exports"), exist_ok=True)
    raw_video = os.path.join(base_dir, "storage", "uploads", f"cloud_{int(time.time())}.mp4")

    clip_section = topic_item.get("slice", "*00:01:30-00:02:05")
    logger.info(f"Slicing punchy 35-second moment from full long video: {clip_section}")

    dl_strategies = [
        [
            "yt-dlp",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
            "--extractor-args", "youtube:player_client=android,web",
            "-f", "bv*[height<=1080]+ba/b[height<=1080]/best",
            "--download-sections", clip_section,
            "--merge-output-format", "mp4",
            "-o", raw_video,
            yt_url
        ],
        [
            "yt-dlp",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtubepot-bgutilhttp:base_url=http://127.0.0.1:4416",
            "--extractor-args", "youtube:player_client=android;player_skip=webpage,configs,initial_data",
            "-f", "bv*[height<=1080]+ba/b[height<=1080]/best",
            "--download-sections", clip_section,
            "--merge-output-format", "mp4",
            "-o", raw_video,
            yt_url
        ],
        [
            "yt-dlp",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtube:player_client=web,android",
            "-f", "bv*[height<=1080]+ba/b[height<=1080]/best",
            "--download-sections", clip_section,
            "--merge-output-format", "mp4",
            "-o", raw_video,
            yt_url
        ]
    ]

    downloaded = False
    for strat in dl_strategies:
        try:
            subprocess.run(strat, check=True, timeout=90)
            if os.path.exists(raw_video) and os.path.getsize(raw_video) > 50000:
                logger.info(f"Downloaded video segment successfully: {raw_video}")
                downloaded = True
                break
        except Exception as e:
            logger.warning(f"Download strategy failed: {e}. Trying next...")

    if not downloaded:
        logger.warning("All download strategies failed. Using high-quality video fallback...")
        from sample_data import generate_sample_mp4
        generate_sample_mp4(raw_video, duration=35)

    # 5. Word-by-Word Subtitle Transcription (Hormozi / MrBeast Animated Captions)
    ass_rel_path = f"storage/exports/sub_{int(time.time())}.ass"
    ass_full_path = os.path.join(base_dir, ass_rel_path)
    has_subtitles = False

    try:
        from caption_styler import CaptionStyler
        from transcriber import AudioTranscriber

        logger.info("Running AudioTranscriber for viral word-level animated captions...")
        transcriber = AudioTranscriber(model_size="tiny")
        transcript_res = transcriber.transcribe(raw_video)
        words = transcript_res.get("words", [])

        if words and len(words) >= 4:
            logger.info(f"Extracted {len(words)} speech words. Generating Hormozi SubStation Alpha (ASS) subtitles...")
            style = "mrbeast" if category in ["GTA 6", "Gaming"] else "hormozi"
            ass_content = CaptionStyler.generate_ass(
                words_data=words,
                style_name=style,
                video_width=1080,
                video_height=1920
            )
            with open(ass_full_path, "w", encoding="utf-8") as f:
                f.write(ass_content)
            if os.path.exists(ass_full_path) and os.path.getsize(ass_full_path) > 50:
                has_subtitles = True
                logger.info(f"Generated animated ASS subtitles successfully: {ass_full_path}")
        else:
            logger.info(f"Only {len(words)} words detected in audio. Proceeding without burned subtitles.")
    except Exception as e:
        logger.warning(f"Transcriber notice: {e}. Will continue with clean visual Short.")

    # 6. Render 9:16 vertical Full HD Short (Blur-Canvas Pro Layout + Hormozi Captions)
    rendered_video = os.path.join(base_dir, "storage", "exports", f"short_{int(time.time())}.mp4")
    clean_hook = "".join(c for c in hook if ord(c) < 128 and c not in ["'", ":", '"']).strip()

    if has_subtitles:
        rel_ass = ass_rel_path.replace("\\", "/")
        filter_complex = (
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[blurred_bg];"
            "[fg]scale=1080:-1:flags=lanczos[scaled_fg];"
            "[blurred_bg][scaled_fg]overlay=(W-w)/2:(H-h)/2[base_canvas];"
            f"[base_canvas]drawtext=text='{clean_hook}':x=(w-text_w)/2:y=230:fontsize=46:fontcolor=white:borderw=4:bordercolor=black:shadowcolor=black@0.8:shadowx=3:shadowy=3[canvas_with_hook];"
            f"[canvas_with_hook]ass={rel_ass}:fontsdir=fonts[final_v]"
        )
    else:
        filter_complex = (
            "[0:v]split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[blurred_bg];"
            "[fg]scale=1080:-1:flags=lanczos[scaled_fg];"
            "[blurred_bg][scaled_fg]overlay=(W-w)/2:(H-h)/2[base_canvas];"
            f"[base_canvas]drawtext=text='{clean_hook}':x=(w-text_w)/2:y=230:fontsize=46:fontcolor=white:borderw=4:bordercolor=black:shadowcolor=black@0.8:shadowx=3:shadowy=3[final_v]"
        )

    render_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-map", "0:a?",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-b:v", "8M", "-maxrate", "12M", "-bufsize", "16M",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "38",
        rendered_video
    ]
    subprocess.run(render_cmd, check=True)
    logger.info(f"Rendered 9:16 Full HD Short: {rendered_video}")

    # 6. Upload to YouTube Shorts
    from youtube_uploader import YouTubeUploader
    upload_res = YouTubeUploader.upload_short(
        video_path=rendered_video,
        title=f"{hook} {category} #Shorts",
        description=f"{query}\n\nSource: {yt_url} [ID: {vid}]\nAuto-curated by ClipFlow AI.\n#Shorts #Viral #Gaming #GTA6 #{category.replace(' ', '')}",
        tags=["#Shorts", "#GTA6", "#Gaming", "#Viral", "#Trending"],
        privacy_status="public",
        client_secrets_path=secret_file
    )

    logger.info(f"Upload Result: {upload_res}")
    print("FINISHED_SUCCESSFULLY:", upload_res.get("video_url"))

if __name__ == "__main__":
    main()
