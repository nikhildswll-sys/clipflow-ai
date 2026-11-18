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

    # --- GTA 6 LIVE STREAM SNIPER POOL (Indian & USA/Global High-Watching Streamers) ---
    GTA6_STREAM_TOPICS = [
        # USA & Global Streamer Titans
        {"category": "GTA 6 Stream", "topic": "IShowSpeed GTA 6 live stream reaction", "hook": "SPEED WENT CRAZY ON GTA 6 🤯", "slice": "*00:01:45-00:02:20"},
        {"category": "GTA 6 Stream", "topic": "Kai Cenat GTA 6 gameplay reaction live stream", "hook": "KAI CENAT CANNOT BELIEVE THIS... 😱", "slice": "*00:02:00-00:02:35"},
        {"category": "GTA 6 Stream", "topic": "xQc GTA 6 trailer gameplay reaction live stream", "hook": "xQc SPOTS INSANE GTA 6 DETAIL 🔍", "slice": "*00:01:30-00:02:05"},
        {"category": "GTA 6 Stream", "topic": "Adin Ross GTA 6 gameplay reaction live stream", "hook": "ADIN ROSS GTA 6 STREAM MOMENT 💀", "slice": "*00:01:40-00:02:15"},
        {"category": "GTA 6 Stream", "topic": "Jynxzi GTA 6 trailer reaction live stream", "hook": "JYNXZI SCREAMS AT GTA 6 🚨", "slice": "*00:01:25-00:02:00"},
        {"category": "GTA 6 Stream", "topic": "Asmongold GTA 6 graphics breakdown live stream", "hook": "THE TRUTH ABOUT GTA 6 GRAPHICS 👁️", "slice": "*00:02:15-00:02:50"},
        {"category": "GTA 6 Stream", "topic": "FlightReacts GTA 6 trailer reaction live stream", "hook": "FLIGHTREACTS SEES GTA 6 😂", "slice": "*00:01:35-00:02:10"},

        # Indian Gaming Royalty (Highest Watching Live)
        {"category": "GTA 6 Stream", "topic": "Techno Gamerz GTA 6 live reaction gameplay stream", "hook": "TECHNO GAMERZ SEES GTA 6 🌴", "slice": "*00:01:50-00:02:25"},
        {"category": "GTA 6 Stream", "topic": "CarryisLive CarryMinati GTA 6 reaction live stream", "hook": "CARRYMINATI GTA 6 REACTION 🔥", "slice": "*00:02:00-00:02:35"},
        {"category": "GTA 6 Stream", "topic": "Total Gaming Ajju007 GTA 6 reaction live stream", "hook": "TOTAL GAMING GTA 6 REACTION 💥", "slice": "*00:01:40-00:02:15"},
        {"category": "GTA 6 Stream", "topic": "Mythpat GTA 6 reaction live stream funny moments", "hook": "MYTHPAT GTA 6 FUNNIEST MOMENT 😂", "slice": "*00:01:30-00:02:05"},
        {"category": "GTA 6 Stream", "topic": "Mortal Scout GTA 6 gameplay reaction live stream", "hook": "MORTAL & SCOUT GTA 6 SHOCK 🚨", "slice": "*00:01:45-00:02:20"},
        {"category": "GTA 6 Stream", "topic": "Triggered Insaan Live GTA 6 reaction stream", "hook": "TRIGGERED INSAAN GTA 6 REACTION 🤯", "slice": "*00:01:35-00:02:10"},

        # Viral Live Stream Events & Highest Watching Clips
        {"category": "GTA 6 Stream", "topic": "GTA 6 live stream high watching top streamer reaction", "hook": "THIS GTA 6 STREAM BROKE YOUTUBE 🚀", "slice": "*00:01:30-00:02:05"},
        {"category": "GTA 6 Stream", "topic": "GTA 6 gameplay live reveal chat reaction", "hook": "THE WHOLE CHAT WENT INSANE... 💬", "slice": "*00:01:20-00:01:55"},
        {"category": "GTA 6 Stream", "topic": "GTA 6 realistic police AI behavior and car crash deformation physics 4K", "hook": "THIS POLICE AI IS TERRIFYING... 🚨", "slice": "*00:01:15-00:01:50"},
        {"category": "GTA 6 Stream", "topic": "GTA 6 Vice City graphics comparison vs real life Miami 4K gameplay", "hook": "VICE CITY VS REAL LIFE 🌴", "slice": "*00:01:30-00:02:05"},
        {"category": "GTA 6 Stream", "topic": "GTA 6 map size comparison vs GTA 5 secret locations breakdown", "hook": "THE MAP IS 3X BIGGER THAN GTA 5 🗺️", "slice": "*00:01:20-00:01:55"},
        {"category": "GTA 6 Stream", "topic": "GTA 6 water physics beach wave simulation and NPC reactions 4k", "hook": "THIS WATER PHYSICS IS UNREAL 🌊", "slice": "*00:01:25-00:02:00"},
        {"category": "GTA 6 Stream", "topic": "GTA 6 2 billion dollar budget why Rockstar took 12 years documentary", "hook": "THE $2,000,000,000 VIDEO GAME 💰", "slice": "*00:01:30-00:02:05"}
    ]

    DEFAULT_TOPICS = [
        # --- 1. GTA 6 Viral Wave (Indian Gamers & Global Leaks / Graphics / Physics) ---
        {"category": "GTA 6", "topic": "GTA 6 realistic police AI behavior and car crash deformation physics 4K", "hook": "THIS POLICE AI IS TERRIFYING... 🚨", "slice": "*00:01:15-00:01:50"},
        {"category": "GTA 6", "topic": "GTA 6 Vice City graphics comparison vs real life Miami 4K gameplay", "hook": "VICE CITY VS REAL LIFE 🌴", "slice": "*00:01:30-00:02:05"},
        {"category": "GTA 6", "topic": "GTA 6 map size comparison vs GTA 5 secret locations breakdown", "hook": "THE MAP IS 3X BIGGER THAN GTA 5 🗺️", "slice": "*00:01:20-00:01:55"},
        {"category": "GTA 6", "topic": "GTA 6 Lucia and Jason story mystery dark secrets gameplay breakdown", "hook": "THE DARK TRUTH OF JASON & LUCIA 💀", "slice": "*00:01:40-00:02:15"},
        {"category": "GTA 6", "topic": "GTA 6 2 billion dollar budget why Rockstar took 12 years documentary", "hook": "THE $2,000,000,000 VIDEO GAME 💰", "slice": "*00:01:30-00:02:05"},
        {"category": "GTA 6", "topic": "GTA 6 water physics beach wave simulation and NPC reactions 4k", "hook": "THIS WATER PHYSICS IS UNREAL 🌊", "slice": "*00:01:25-00:02:00"},
        {"category": "GTA 6", "topic": "GTA 6 weapon mechanics gore and shooting physics leaked gameplay breakdown", "hook": "GTA 6 GUNPLAY DETAILS LEAKED 💥", "slice": "*00:01:10-00:01:45"},

        # --- 2. High-Retention Podcasts (Indian & Global Speech / Animated Captions) ---
        {"category": "Podcast", "topic": "Ranveer Allahbadia BeerBiceps secret ancient temple mystery breakdown", "hook": "THE SECRET OF ANCIENT TEMPLES 🕉️", "slice": "*00:02:00-00:02:35"},
        {"category": "Podcast", "topic": "Raj Shamani podcast cyber security expert how hackers tap your phone", "hook": "HOW THEY ARE SPYING ON YOUR PHONE 📱", "slice": "*00:01:45-00:02:20"},
        {"category": "Podcast", "topic": "Joe Rogan Neil deGrasse Tyson what happens inside black hole time dilation", "hook": "TIME STOPS INSIDE A BLACK HOLE ⏳", "slice": "*00:01:30-00:02:05"},
        {"category": "Podcast", "topic": "Joe Rogan Lex Fridman artificial intelligence superintelligence singularity warning", "hook": "AI WILL SURPASS HUMAN INTELLIGENCE 🤖", "slice": "*00:01:50-00:02:25"},
        {"category": "Podcast", "topic": "Andrew Huberman dopamine reset rewire brain science protocol", "hook": "HOW TO REWIRE YOUR BRAIN IN 48 HOURS ⚡", "slice": "*00:02:10-00:02:45"},
        {"category": "Podcast", "topic": "Neil deGrasse Tyson explains simulation theory mind blowing interview", "hook": "ARE WE LIVING IN A SIMULATION? 👁️", "slice": "*00:01:35-00:02:10"},

        # --- 3. Sci-Fi & Cosmic Mysteries (Insane Visuals & Mind Expansion) ---
        {"category": "Sci-Fi", "topic": "James Webb telescope discovered impossible massive structure in deep space visualization", "hook": "NASA DIDNT EXPECT TO FIND THIS 🔭", "slice": "*00:01:40-00:02:15"},
        {"category": "Sci-Fi", "topic": "black hole accretion disk 4K simulation interstellar crossing event horizon", "hook": "WHAT HAPPENS INSIDE A BLACK HOLE? 🕳️", "slice": "*00:01:20-00:01:55"},
        {"category": "Sci-Fi", "topic": "scale of the universe 3D 4k mind blowing cosmic comparison", "hook": "HOW TINY ARE WE REALLY? 🌌", "slice": "*00:01:15-00:01:50"},
        {"category": "Sci-Fi", "topic": "solar superstorm Carrington event hitting modern earth simulation NASA", "hook": "WHAT A SOLAR STORM DOES TO EARTH ⚡", "slice": "*00:01:30-00:02:05"},
        {"category": "Sci-Fi", "topic": "future mars colony 2050 4K realistic simulation life in space", "hook": "LIFE ON MARS IN 2050 🚀", "slice": "*00:01:25-00:02:00"},

        # --- 4. History & Ancient Mysteries (Indian & World) ---
        {"category": "History", "topic": "Kailash Temple rock-cut architecture mystery carved top to bottom impossible engineering", "hook": "IMPOSSIBLE ANCIENT ENGINEERING 🏛️", "slice": "*00:01:50-00:02:25"},
        {"category": "History", "topic": "deadly curse of the Kohinoor Diamond every king who possessed it documentary", "hook": "THE DEADLY CURSE OF KOHINOOR 💎", "slice": "*00:02:00-00:02:35"},
        {"category": "History", "topic": "Indus Valley Civilization script mystery why nobody can decode it", "hook": "THE UNDECODED ANCIENT SCRIPT 📜", "slice": "*00:01:35-00:02:10"},
        {"category": "History", "topic": "Great Pyramid of Giza secret chambers and Orion constellation alignment documentary", "hook": "WHAT LIES INSIDE THE PYRAMIDS? 🔍", "slice": "*00:01:45-00:02:20"},
        {"category": "History", "topic": "lost city of Atlantis underwater satellite scan discovery mystery", "hook": "SECRET BEHIND ATLANTIS DISCOVERY ⚓", "slice": "*00:01:30-00:02:05"},

        # --- 5. Kids & Curiosity Wonders (Prehistoric, Animals & Deep Earth) ---
        {"category": "Wonders", "topic": "asteroid impact simulation that wiped out dinosaurs 66 million years ago 4K", "hook": "THE DAY THE ASTEROID HIT EARTH ☄️", "slice": "*00:01:20-00:01:55"},
        {"category": "Wonders", "topic": "Megalodon vs Blue Whale scale comparison terror of prehistoric oceans 3D", "hook": "THE BIGGEST PREDATOR IN HISTORY 🦈", "slice": "*00:01:15-00:01:50"},
        {"category": "Wonders", "topic": "deep sea Mariana Trench terrifying creatures surviving extreme pressure NOAA", "hook": "ALIEN CREATURES IN THE DEEP SEA 🌊", "slice": "*00:01:30-00:02:05"},
        {"category": "Wonders", "topic": "immortal jellyfish Turritopsis dohrnii reverses its age forever science", "hook": "THE ANIMAL THAT NEVER DIES 🪼", "slice": "*00:01:25-00:02:00"}
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
