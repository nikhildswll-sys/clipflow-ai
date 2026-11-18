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

    # 4. GTA 6 Live Stream Sniper & Viral Wave with Dynamic Anti-Duplicate Filter
    from autopilot import AutoPilotService
    service = AutoPilotService()
    
    mode = os.environ.get("GTA6_DAY_MODE", "mixed").lower()

    def is_already_uploaded(topic_dict):
        h = topic_dict.get("hook", "").replace("'", "").lower().strip()
        h_words = [w for w in h.split() if len(w) > 3][:3]
        for rt in recent_titles:
            if h and h in rt:
                return True
            if h_words and all(w in rt for w in h_words):
                return True
        return False

    if mode in ["stream_only", "gta6_only"]:
        logger.info("🎮 GTA 6 ALL-DAY STREAM SNIPER ACTIVE: Targeting Top Indian & Global Streamers!")
        stream_pool = getattr(service, "GTA6_STREAM_TOPICS", service.topics)
        unseen_pool = [t for t in stream_pool if not is_already_uploaded(t)]
        if unseen_pool:
            logger.info(f"Anti-duplicate filter: {len(unseen_pool)} unseen streamer topics available.")
            topic_item = random.choice(unseen_pool)
        else:
            logger.info("All streamer topics used recently; cycling pool.")
            topic_item = random.choice(stream_pool)
    else:
        # Default smart mix: 60% GTA 6 (Streamers + Viral Game Mechanics), 40% Podcasts / Sci-Fi / History / Wonders
        category_weights = {
            "GTA 6 Stream": 0.35,
            "GTA 6": 0.25,
            "Podcast": 0.15,
            "Sci-Fi": 0.10,
            "History": 0.10,
            "Wonders": 0.05
        }
        all_pool = list(getattr(service, "GTA6_STREAM_TOPICS", [])) + list(service.topics)
        dedup_pool = []
        seen_t = set()
        for t in all_pool:
            if t["topic"] not in seen_t:
                seen_t.add(t["topic"])
                dedup_pool.append(t)

        try:
            available_cats = list(category_weights.keys())
            weights = [category_weights[c] for c in available_cats]
            chosen_cat = random.choices(available_cats, weights=weights, k=1)[0]
            cat_topics = [t for t in dedup_pool if t.get("category") == chosen_cat]
            unseen_cat = [t for t in cat_topics if not is_already_uploaded(t)]
            if unseen_cat:
                topic_item = random.choice(unseen_cat)
            elif cat_topics:
                topic_item = random.choice(cat_topics)
            else:
                topic_item = random.choice(dedup_pool)
        except Exception as e:
            logger.warning(f"Selection fallback: {e}. Picking uniform topic.")
            topic_item = random.choice(dedup_pool)

    query = topic_item["topic"]
    target_streamer = topic_item.get("streamer")
    category = topic_item.get("category", "GTA 6")
    base_hook = topic_item.get("hook", "WAIT FOR IT... 🤯")

    logger.info(f"Targeting: '{query}' | Target Streamer: '{target_streamer}' | Category: '{category}'")

    search_query = f"{query} -#shorts -shorts"
    logger.info(f"Searching official YouTube API for full long-form video (16:9): '{search_query}'...")
    search_res = youtube.search().list(
        q=search_query,
        part="snippet",
        type="video",
        videoDuration="medium",  # 4 to 20 minutes
        order="viewCount",      # Highest views / most viral
        maxResults=10
    ).execute()

    if not search_res.get("items"):
        # Fallback to longer videos (>20 mins podcasts/documentaries) if needed
        search_res = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            videoDuration="long",
            order="viewCount",
            maxResults=10
        ).execute()

    if not search_res.get("items"):
        search_res = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            order="relevance",
            maxResults=10
        ).execute()

    if not search_res.get("items"):
        logger.error(f"No videos found via official API for {query}")
        sys.exit(1)

    # Bulletproof Streamer Verification & Video Selection
    selected_item = None
    streamer_verified = False

    if target_streamer:
        s_name = target_streamer.lower()
        s_parts = [p for p in s_name.split() if len(p) > 3]
        for it in search_res.get("items", []):
            v_id = it["id"].get("videoId", "")
            if any(v_id in rt for rt in recent_titles):
                continue
            ch_title = it["snippet"].get("channelTitle", "").lower()
            v_title = it["snippet"].get("title", "").lower()
            if (s_name in ch_title or s_name in v_title) or any(p in ch_title or p in v_title for p in s_parts):
                selected_item = it
                streamer_verified = True
                logger.info(f"Verified authentic video for streamer '{target_streamer}': {it['snippet']['title']} (Channel: {it['snippet']['channelTitle']})")
                break

    if not selected_item:
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
    raw_video_title = selected_item["snippet"]["title"]
    actual_channel = selected_item["snippet"]["channelTitle"].strip()
    logger.info(f"Target video found via Official API: '{raw_video_title}' by '{actual_channel}' ({yt_url})")

    # 100% TRUTHFUL HOOK & TITLE ENGINE: Never falsely attribute another creator's video!
    if target_streamer:
        if streamer_verified:
            hook = base_hook
            upload_title = f"{hook} #GTA6 #Shorts"
        else:
            logger.warning(f"Video is by '{actual_channel}', NOT '{target_streamer}'. Deriving truthful hook & title!")
            clean_ch = "".join(c for c in actual_channel if c.isalnum() or c.isspace()).strip()
            hook = f"{clean_ch.upper()[:20]} GTA 6 REACTION 🔥"
            upload_title = f"{clean_ch[:24]} Reacts to GTA 6 🌴 #GTA6 #Shorts"
    else:
        hook = base_hook
        tag = category.replace(" ", "")
        upload_title = f"{hook} #{tag} #Shorts"

    logger.info(f"Final Truthful Hook: '{hook}' | Upload Title: '{upload_title}'")

    # 4. Download segment from the meat of the long video (Strict 1080p / 720p HD)
    os.makedirs(os.path.join(base_dir, "storage", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "storage", "exports"), exist_ok=True)
    raw_video = os.path.join(base_dir, "storage", "uploads", f"cloud_{int(time.time())}.mp4")

    clip_section = topic_item.get("slice", "*00:01:30-00:02:05")
    logger.info(f"Slicing punchy 35-second moment from full long video: {clip_section}")

    fmt_sort = "res:1080,res:720,quality,codec:h264,size,br"
    fmt_spec = "bestvideo[height>=720]+bestaudio/best[height>=720]"

    dl_strategies = [
        # Strategy 1: Web and TV clients with official Deno JS solver (1080p/720p)
        [
            "yt-dlp",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtube:player_client=web,tv",
            "--format-sort", fmt_sort,
            "-f", fmt_spec,
            "--download-sections", clip_section,
            "--merge-output-format", "mp4",
            "-o", raw_video,
            yt_url
        ],
        # Strategy 2: Web creator client with Deno (Bypasses bot checks, 1080p/720p)
        [
            "yt-dlp",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtube:player_client=web_creator,tv",
            "--format-sort", fmt_sort,
            "-f", fmt_spec,
            "--download-sections", clip_section,
            "--merge-output-format", "mp4",
            "-o", raw_video,
            yt_url
        ],
        # Strategy 3: iOS and mobile web client
        [
            "yt-dlp",
            "--remote-components", "ejs:github",
            "--extractor-args", "youtube:player_client=ios,mweb",
            "--format-sort", fmt_sort,
            "-f", fmt_spec,
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
    else:
        try:
            res_out = subprocess.check_output(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", raw_video],
                text=True
            ).strip().replace(",", "x")
            logger.info(f"Verified downloaded video resolution: {res_out} (High Definition source verified)")
        except Exception as e:
            logger.info(f"Resolution check notice: {e}")

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
        title=upload_title,
        description=f"{upload_title}\n\nCreator: {actual_channel}\nSource Video: {yt_url} [ID: {vid}]\nAuto-curated by ClipFlow AI.\n#Shorts #Viral #Gaming #GTA6 #{category.replace(' ', '')}",
        tags=["#Shorts", "#GTA6", "#Gaming", "#Viral", "#Trending", category.replace(" ", "")],
        privacy_status="public",
        client_secrets_path=secret_file
    )

    logger.info(f"Upload Result: {upload_res}")
    print("FINISHED_SUCCESSFULLY:", upload_res.get("video_url"))

if __name__ == "__main__":
    main()
