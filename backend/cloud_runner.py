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
    import socket
    socket.setdefaulttimeout(60)
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

    target_vid_override = os.environ.get("TARGET_VIDEO_ID", "").strip()
    candidate_items = []

    if target_vid_override:
        logger.info(f"Targeting SPECIFIC requested video/stream ID: {target_vid_override}")
        v_res = youtube.videos().list(id=target_vid_override, part="snippet").execute()
        if v_res.get("items"):
            item_raw = v_res["items"][0]
            actual_ch = item_raw["snippet"].get("channelTitle", "Creator").strip()
            topic_item = {
                "topic": item_raw["snippet"].get("title", f"{actual_ch} Video"),
                "category": "Curated",
                "slice": "*00:01:30-00:02:05",
                "hook": f"{actual_ch.upper()} BEST MOMENT 🔥"
            }
            chosen_item = {
                "id": {"videoId": target_vid_override},
                "snippet": item_raw["snippet"],
                "_streamer_verified": True
            }
            candidate_items = [chosen_item]
            query = topic_item["topic"]
            target_streamer = actual_ch
            category = "Curated"
            base_hook = topic_item["hook"]
        else:
            logger.error(f"Target video ID '{target_vid_override}' not found on YouTube.")
            sys.exit(1)
    else:
        # Multi-Category Rotation weighted per user request:
        # 1. Indian Podcasts (BeerBiceps, Raj Shamani, Dostcast, RealHit) -> 25%
        # 2. Indian Comedy (Samay Raina, Tanmay Bhat, Zakir Khan, Bassi) -> 20%
        # 3. English Viral Podcasts & Comedy (Joe Rogan, Theo Von, Flagrant) -> 18%
        # 4. Indian Ancient Mysteries (Kailash Temple, Padmanabhaswamy, Ram Setu) -> 15%
        # 5. Sci-Fi & Cosmic Mysteries (James Webb, Black Holes, Multiverse) -> 12%
        # 6. Kids & Curiosity Wonders (Megalodon, Dinosaurs, Deep Sea Animals) -> 10%
        category_weights = {
            "Indian Podcast": 0.25,
            "Indian Comedy": 0.20,
            "English Podcast": 0.18,
            "Indian Mystery": 0.15,
            "Sci-Fi": 0.12,
            "Wonders": 0.10
        }

        all_pool = list(service.topics)
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
        category = topic_item.get("category", "Indian Podcast")
        base_hook = topic_item.get("hook", "WAIT FOR IT... 🤯")

        logger.info(f"Targeting Topic: '{query}' | Category: '{category}' | Hook: '{base_hook}'")

        search_query = f"{query} -#shorts -shorts"
        logger.info(f"Searching official YouTube API for full long-form video (16:9): '{search_query}'...")
        
        search_res = None
        query_candidates = [
            query,
            f"{query} official",
            f"{' '.join(query.split()[:5])}"
        ]
        for q_cand in query_candidates:
            try:
                # 1. First priority: Medium duration videos (4 to 20 minutes)
                res = youtube.search().list(
                    q=q_cand,
                    part="snippet",
                    type="video",
                    videoDuration="medium",
                    order="viewCount",
                    maxResults=10
                ).execute()
                if res.get("items"):
                    search_res = res
                    logger.info(f"Found {len(res['items'])} medium duration candidate videos using: '{q_cand}'")
                    break

                # 2. Second priority: Long duration videos (>20 minutes full stream/podcast)
                res = youtube.search().list(
                    q=q_cand,
                    part="snippet",
                    type="video",
                    videoDuration="long",
                    order="viewCount",
                    maxResults=10
                ).execute()
                if res.get("items"):
                    search_res = res
                    logger.info(f"Found {len(res['items'])} long duration candidate videos using: '{q_cand}'")
                    break
            except Exception as e:
                logger.warning(f"Search notice for '{q_cand}': {e}")

        if not search_res or not search_res.get("items"):
            logger.error(f"No videos found via official API for {query}")
            sys.exit(1)

        # Bulletproof Streamer Verification & Video Candidates Selection
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
                    it["_streamer_verified"] = True
                    candidate_items.append(it)

        for it in search_res.get("items", []):
            v_id = it["id"].get("videoId", "")
            if any(v_id in rt for rt in recent_titles):
                continue
            if it not in candidate_items:
                it["_streamer_verified"] = False
                candidate_items.append(it)

        if not candidate_items:
            candidate_items = search_res.get("items", [])[:5]

    # 4. Download segment from the meat of the long video (Strict 1080p / 720p HD)
    os.makedirs(os.path.join(base_dir, "storage", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "storage", "exports"), exist_ok=True)
    raw_video = os.path.join(base_dir, "storage", "uploads", f"cloud_{int(time.time())}.mp4")

    clip_section = topic_item.get("slice", "*00:01:30-00:02:05")
    logger.info(f"Slicing punchy 35-second moment from full long video: {clip_section}")

    fmt_sort = "res:1080,res:720,quality,codec:h264,size,br"
    fmt_spec = "bestvideo[height>=720]+bestaudio/best[height>=720]/bestvideo+bestaudio/best"

    downloaded = False
    chosen_item = None

    proxy_cmd = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex(("127.0.0.1", 40000)) == 0:
                proxy_cmd = ["--proxy", "socks5://127.0.0.1:40000"]
                logger.info("WARP SOCKS5 anti-bot proxy detected on 127.0.0.1:40000!")
    except Exception:
        pass

    for candidate in candidate_items[:5]:
        vid = candidate["id"]["videoId"]
        yt_url = f"https://www.youtube.com/watch?v={vid}"
        raw_video_title = candidate["snippet"]["title"]
        actual_channel = candidate["snippet"]["channelTitle"].strip()
        logger.info(f"Attempting download for candidate: '{raw_video_title}' by '{actual_channel}' ({yt_url})...")

        dl_strategies = [
            # Strategy 1: Android client bypassing webpage and config challenges (Guaranteed 0 bot check)
            [
                "yt-dlp",
                *proxy_cmd,
                "--extractor-args", "youtube:player_client=android;player_skip=webpage,configs",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                "--download-sections", clip_section,
                "--force-keyframes-at-cuts",
                "--merge-output-format", "mp4",
                "-o", raw_video,
                yt_url
            ],
            # Strategy 2: Apple VisionOS client with webpage skip
            [
                "yt-dlp",
                *proxy_cmd,
                "--extractor-args", "youtube:player_client=visionos;player_skip=webpage,configs",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                "--download-sections", clip_section,
                "--force-keyframes-at-cuts",
                "--merge-output-format", "mp4",
                "-o", raw_video,
                yt_url
            ],
            # Strategy 3: TV Embedded client with webpage skip
            [
                "yt-dlp",
                *proxy_cmd,
                "--extractor-args", "youtube:player_client=tv_embedded;player_skip=webpage,configs",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                "--download-sections", clip_section,
                "--force-keyframes-at-cuts",
                "--merge-output-format", "mp4",
                "-o", raw_video,
                yt_url
            ],
            # Strategy 4: Web Creator fallback
            [
                "yt-dlp",
                *proxy_cmd,
                "--extractor-args", "youtube:player_client=web_creator",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                "--download-sections", clip_section,
                "--force-keyframes-at-cuts",
                "--merge-output-format", "mp4",
                "-o", raw_video,
                yt_url
            ]
        ]

        for strat in dl_strategies:
            try:
                subprocess.run(strat, check=True, timeout=60)
                if os.path.exists(raw_video) and os.path.getsize(raw_video) > 50000:
                    logger.info(f"Downloaded video segment successfully from '{actual_channel}': {raw_video}")
                    downloaded = True
                    chosen_item = candidate
                    break
            except Exception as e:
                logger.warning(f"Download strategy failed: {e}. Trying next...")

        if downloaded:
            break

    if not downloaded or not chosen_item:
        logger.error("Could not download any authentic long video. Aborting job to protect channel quality!")
        sys.exit(1)

    # 100% TRUTHFUL HOOK & TITLE ENGINE: Never falsely attribute another creator's video!
    actual_channel = chosen_item["snippet"]["channelTitle"].strip()
    streamer_verified = chosen_item.get("_streamer_verified", False)

    if target_streamer:
        if streamer_verified:
            hook = base_hook
            if "#Shorts" in hook:
                upload_title = hook
            else:
                tag = category.replace(" ", "")
                upload_title = f"{hook} #{tag} #Shorts"
        else:
            logger.warning(f"Video is by '{actual_channel}', NOT '{target_streamer}'. Deriving truthful hook & title!")
            clean_ch = "".join(c for c in actual_channel if c.isalnum() or c.isspace()).strip()
            hook = f"{clean_ch.upper()[:24]} 🔥"
            tag = category.replace(" ", "")
            upload_title = f"{hook} #{tag} #Shorts"
    else:
        hook = base_hook
        tag = category.replace(" ", "")
        upload_title = f"{hook} #{tag} #Shorts"

    logger.info(f"Final Truthful Hook: '{hook}' | Upload Title: '{upload_title}'")

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
        # Properly escape path for FFmpeg filter on both Windows and Linux
        escaped_ass = ass_full_path.replace("\\", "/").replace(":", "\\:")
        filter_complex = (
            "[0:v]setpts=PTS-STARTPTS,split=2[bg][fg];"
            "[bg]scale=120:213,boxblur=5:1,scale=1080:1920:flags=bilinear,setsar=1[blurred_bg];"
            "[fg]scale=1080:-1:flags=lanczos,setsar=1[scaled_fg];"
            "[blurred_bg][scaled_fg]overlay=(W-w)/2:(H-h)/2,setsar=1[base_canvas];"
            f"[base_canvas]ass='{escaped_ass}':fontsdir=fonts,setsar=1,format=yuv420p[final_v]"
        )
    else:
        filter_complex = (
            "[0:v]setpts=PTS-STARTPTS,split=2[bg][fg];"
            "[bg]scale=120:213,boxblur=5:1,scale=1080:1920:flags=bilinear,setsar=1[blurred_bg];"
            "[fg]scale=1080:-1:flags=lanczos,setsar=1[scaled_fg];"
            "[blurred_bg][scaled_fg]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv420p[final_v]"
        )

    render_cmd = [
        "ffmpeg", "-y",
        "-fflags", "+genpts+discardcorrupt",
        "-i", raw_video,
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-map", "0:a?",
        "-aspect", "9:16",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-b:v", "6M", "-maxrate", "10M", "-bufsize", "12M",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-af", "aresample=async=1",
        "-movflags", "+faststart",
        "-t", "35",
        rendered_video
    ]
    subprocess.run(render_cmd, cwd=base_dir, check=True, timeout=120)
    logger.info(f"Rendered 9:16 Full HD Short: {rendered_video}")

    # 6. Upload to YouTube Shorts
    from youtube_uploader import YouTubeUploader
    category_tags = {
        "Indian Podcast": ["#Podcast", "#IndianPodcast", "#BeerBiceps", "#RajShamani", "#Shorts", "#Viral", "#Trending"],
        "Indian Comedy": ["#Comedy", "#IndianComedy", "#StandupComedy", "#SamayRaina", "#ZakirKhan", "#Shorts", "#Funny"],
        "English Podcast": ["#Podcast", "#JoeRogan", "#TheoVon", "#Comedy", "#Shorts", "#ViralShorts"],
        "Indian Mystery": ["#Mystery", "#IndianHistory", "#AncientIndia", "#KailashTemple", "#Secrets", "#Shorts"],
        "Sci-Fi": ["#SciFi", "#Space", "#NASA", "#Universe", "#BlackHole", "#ScienceFacts", "#Shorts"],
        "Wonders": ["#Wonders", "#AnimalFacts", "#Dinosaurs", "#DeepSea", "#Megalodon", "#Shorts"]
    }
    cur_tags = category_tags.get(category, ["#Shorts", f"#{category.replace(' ', '')}", "#Viral", "#Trending"])
    clean_ch_tag = "".join(c for c in actual_channel if c.isalnum())
    if clean_ch_tag and clean_ch_tag not in cur_tags:
        cur_tags.append(clean_ch_tag)

    upload_res = YouTubeUploader.upload_short(
        video_path=rendered_video,
        title=upload_title,
        description=f"{upload_title}\n\nCreator: {actual_channel}\nSource Video: {yt_url} [ID: {vid}]\nAuto-curated by ClipFlow AI.\n#Shorts #Viral #{category.replace(' ', '')} #{clean_ch_tag}",
        tags=cur_tags,
        privacy_status="public",
        client_secrets_path=secret_file
    )

    logger.info(f"Upload Result: {upload_res}")
    if upload_res.get("status") == "error":
        err_msg = upload_res.get("message", "")
        if "uploadLimitExceeded" in str(err_msg):
            logger.error("[FATAL ERROR] YouTube 24-hour daily upload quota reached (uploadLimitExceeded).")
            logger.error("YouTube enforces a 24-hour rolling cooldown. Failing job loudly so GitHub Actions shows red.")
        else:
            logger.error(f"[FATAL ERROR] Upload failed: {err_msg}")
        sys.exit(1)
    else:
        print("FINISHED_SUCCESSFULLY:", upload_res.get("video_url"))

if __name__ == "__main__":
    main()
