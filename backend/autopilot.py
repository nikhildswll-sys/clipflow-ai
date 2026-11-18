import os
import time
import json
import uuid
import logging
import threading
from typing import List, Dict, Any, Optional
import subprocess

logger = logging.getLogger("AutoPilot")

class AutoPilotService:
    """
    Automated YouTube Shorts Pipeline:
    - Automatically cycles through high-retention viral topics (GTA 6, Sci-Fi, Mysteries, Tech)
    - Searches and ingests videos using yt-dlp
    - Runs Faster-Whisper & single viral clip detector
    - Auto-frames into 9:16 Shorts with Hormozi Clean bottom captions (no box)
    - Automatically uploads to YouTube Shorts every 30 minutes!
    """

    DEFAULT_TOPICS = [
        # GTA 6 Viral Topic Queue (Massive CTR & Trending)
        {"category": "GTA 6", "topic": "GTA 6 leaked gameplay insane physics and graphics details", "hook": "GTA 6 JUST BROKE REALITY... 🤯"},
        {"category": "GTA 6", "topic": "GTA 6 Vice City map comparison size vs GTA 5 secret locations", "hook": "THE MAP IS 3X BIGGER THAN GTA 5 🗺️"},
        {"category": "GTA 6", "topic": "GTA 6 Lucia and Jason story mystery breakdown", "hook": "THE DARK TRUTH ABOUT JASON & LUCIA 💀"},
        {"category": "GTA 6", "topic": "GTA 6 hyper realistic police AI and NPC reaction leaks", "hook": "THIS POLICE AI IS TERRIFYING... 🚨"},
        {"category": "GTA 6", "topic": "Rockstar Games secret detail in GTA 6 trailer nobody saw", "hook": "LOOK AT WHAT ROCKSTAR HID HERE... 🔍"},

        # Sci-Fi & Universe Mysteries (High Retention)
        {"category": "Sci-Fi", "topic": "James Webb telescope discovered impossible giant structure in deep space", "hook": "NASA DIDN'T EXPECT TO FIND THIS... 🔭"},
        {"category": "Sci-Fi", "topic": "Black hole time dilation paradox explained simply", "hook": "1 HOUR HERE IS 7 YEARS ON EARTH ⏳"},
        {"category": "Sci-Fi", "topic": "Scientist explains why we definitely live in a simulation", "hook": "THE GLITCH IN REALITY EXPOSED 👁️"},
        {"category": "Sci-Fi", "topic": "Voyager 1 received mysterious signal from outside solar system", "hook": "WHAT VOYAGER HEARD IN DEEP SPACE 🛸"},

        # Mind-Blowing AI & Tech Disclosures
        {"category": "AI & Tech", "topic": "Humanoid robot agility and AI consciousness debate", "hook": "THEY ARE ALREADY FASTER THAN HUMANS 🤖"},
        {"category": "AI & Tech", "topic": "Neuralink patient controls computer with brain thoughts", "hook": "TELEPATHY IS ACTUALLY REAL NOW 🧠"},
        {"category": "AI & Tech", "topic": "Quantum computers breaking all encryption codes in minutes", "hook": "EVERY PASSWORD COULD BE USELESS SOON 💻"},

        # Psychology & Crazy Real Secrets
        {"category": "Mind Secrets", "topic": "Dark psychology tricks casino use to make you lose money", "hook": "THE DIRTY CASINO TRICK NOBODY KNOWS 🎰"},
        {"category": "Mind Secrets", "topic": "Dopamine detox neurological transformation after 7 days", "hook": "HOW REWIRING YOUR BRAIN CHANGES EVERYTHING ⚡"}
    ]

    def __init__(self, interval_seconds: int = 1800, privacy_status: str = "public"):
        self.interval_seconds = interval_seconds # 30 minutes = 1800s
        self.privacy_status = privacy_status     # 'public', 'unlisted', or 'private'
        self.is_running = False
        self.current_topic_index = 0
        self.thread: Optional[threading.Thread] = None
        self.history: List[Dict[str, Any]] = []
        self.last_run_time: Optional[float] = None
        self.next_run_time: Optional[float] = None
        self.current_status: str = "idle"
        self.topics = list(self.DEFAULT_TOPICS)

    def get_status(self) -> Dict[str, Any]:
        seconds_remaining = 0
        if self.is_running and self.next_run_time:
            seconds_remaining = max(0, int(self.next_run_time - time.time()))

        return {
            "is_running": self.is_running,
            "interval_seconds": self.interval_seconds,
            "interval_minutes": self.interval_seconds // 60,
            "current_status": self.current_status,
            "seconds_remaining": seconds_remaining,
            "total_topics_queued": len(self.topics),
            "current_topic": self.topics[self.current_topic_index % len(self.topics)] if self.topics else None,
            "privacy_status": self.privacy_status,
            "total_uploaded": len(self.history),
            "history": self.history[-10:] # last 10 uploads
        }

    def start(self, interval_minutes: int = 30, privacy_status: str = "public") -> Dict[str, Any]:
        if self.is_running:
            return {"status": "already_running", "message": "AutoPilot scheduler is already active."}

        self.interval_seconds = max(60, interval_minutes * 60)
        self.privacy_status = privacy_status
        self.is_running = True
        self.current_status = "scheduled"
        self.next_run_time = time.time() + 10 # Trigger first run in 10s

        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logger.info(f"AutoPilot service started with {interval_minutes}m interval.")
        return {"status": "started", "interval_minutes": interval_minutes, "privacy": privacy_status}

    def stop(self) -> Dict[str, Any]:
        self.is_running = False
        self.current_status = "stopped"
        self.next_run_time = None
        logger.info("AutoPilot service stopped.")
        return {"status": "stopped"}

    def add_custom_topic(self, topic: str, category: str = "Custom", hook: str = "DON'T MISS THIS... 🚀"):
        item = {"category": category, "topic": topic, "hook": hook}
        self.topics.insert(0, item) # Insert at head so it runs next
        return {"status": "added", "topic": item}

    def _run_loop(self):
        while self.is_running:
            now = time.time()
            if self.next_run_time and now >= self.next_run_time:
                try:
                    self._execute_cycle()
                except Exception as e:
                    logger.error(f"Error in AutoPilot cycle: {e}")
                    self.current_status = f"error: {str(e)[:100]}"
                
                if self.is_running:
                    self.next_run_time = time.time() + self.interval_seconds
                    self.current_status = f"waiting (next in {self.interval_seconds // 60}m)"

            time.sleep(2)

    def _execute_cycle(self):
        if not self.topics:
            return

        topic_item = self.topics[self.current_topic_index % len(self.topics)]
        self.current_topic_index += 1
        query = topic_item["topic"]
        hook_text = topic_item.get("hook", "WAIT FOR IT... 🤯")
        category = topic_item.get("category", "Trending")

        self.current_status = f"searching: {query}"
        logger.info(f"AutoPilot searching for: '{query}' ({category})")

        # 1. Search for top viral short clip / podcast / video on YouTube using yt-dlp
        search_cmd = [
            "yt-dlp",
            f"ytsearch1:{query}",
            "--dump-json",
            "--no-playlist"
        ]
        try:
            res = subprocess.run(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            if res.returncode != 0 or not res.stdout.strip():
                logger.warning(f"No search results for '{query}'")
                return
            video_info = json.loads(res.stdout.strip().splitlines()[0])
            yt_url = video_info.get("webpage_url") or video_info.get("url")
            title = video_info.get("title", query)
            logger.info(f"AutoPilot selected video: {title} ({yt_url})")
        except Exception as e:
            logger.error(f"Search failed for {query}: {e}")
            return

        # 2. Trigger ClipFlow AI pipeline
        self.current_status = f"processing: {title[:35]}..."
        try:
            from main import import_youtube_video, process_project_pipeline, render_clip, RenderClipRequest, YouTubeUploadRequest, upload_to_youtube
            from main import StreamRequest, PROJECTS_DB

            req = StreamRequest(stream_url=yt_url, auto_generate=True)
            proj = import_youtube_video(req)
            proj_id = proj["id"]

            # Wait / verify clips were generated
            full_proj = PROJECTS_DB.get(proj_id, {})
            clips = full_proj.get("clips", [])
            if not clips:
                logger.warning(f"No viral clips generated for project {proj_id}")
                return

            best_clip = clips[0] # The #1 viral clip
            clip_id = best_clip["id"]

            # 3. Render 9:16 vertical Short with Hormozi Clean captions & bottom position
            self.current_status = f"rendering 9:16 Short: {best_clip.get('title', 'Clip')[:30]}"
            render_req = RenderClipRequest(
                project_id=proj_id,
                clip_id=clip_id,
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
            rendered_video_path = render_res.get("file_path")

            if not rendered_video_path or not os.path.exists(rendered_video_path):
                logger.error(f"Render failed for clip {clip_id}")
                return

            # 4. Upload to YouTube Shorts
            self.current_status = f"uploading to YouTube Shorts..."
            upload_title = f"{hook_text} {topic_item.get('category', '')}".strip()
            upload_req = YouTubeUploadRequest(
                video_path=rendered_video_path,
                title=upload_title[:95],
                description=f"{query}\n\nAuto-clipped by ClipFlow AI.\n#Shorts #Viral #Gaming #GTA6 #{category.replace(' ', '')}",
                tags=["#Shorts", "#GTA6", "#Gaming", "#Viral", "#Trending", f"#{category}"],
                privacy_status=self.privacy_status
            )
            upload_res = upload_to_youtube(upload_req)

            record = {
                "id": str(uuid.uuid4())[:8],
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "topic": query,
                "category": category,
                "title": upload_title,
                "youtube_url": upload_res.get("youtube_url", ""),
                "status": upload_res.get("status", "unknown"),
                "rendered_file": os.path.basename(rendered_video_path)
            }
            self.history.append(record)
            logger.info(f"AutoPilot upload completed: {record}")

        except Exception as e:
            logger.error(f"Error during AutoPilot execution: {e}")
            self.current_status = f"error: {str(e)[:80]}"

autopilot_service = AutoPilotService(interval_seconds=1800)
