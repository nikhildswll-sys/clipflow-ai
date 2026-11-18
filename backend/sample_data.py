import os
import subprocess
from typing import Dict, Any, List

DEMO_PROJECTS = [
    {
        "id": "demo_podcast_01",
        "title": "The AI Revolution & The Future of Human Brain (Deep Dive)",
        "source_type": "youtube",
        "duration": 184.0,
        "language": "en",
        "speaker_count": 2,
        "speakers": ["Lex Fridman", "Elon Musk"],
        "thumbnail": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&auto=format&fit=crop&q=80",
        "transcript": {
            "language": "en",
            "duration": 184.0,
            "text": "The absolute craziest thing happened when we started this journey. Nobody believed that AI could literally cut 3-hour podcasts into viral shorts in 10 seconds. Look at MrBeast, Joe Rogan, Lex Fridman. Their short clips get 10 times more views than full episodes! Wait, do you actually think short-form content is destroying long-form attention spans? That is a complete myth! Short clips actually act as the top of the funnel to bring millions of people back into deep 3-hour conversations. If you are not repurposing your streams right now, you are leaving 90% of your audience on the table. The secret is the hook. In the first 3 seconds, if you don't shock them or make them curious, they swipe away. And animated captions increase watch retention by over 380 percent. People watch on mute! Never ever cut off a sentence mid-thought. The punchline has to land cleanly. Boom! That is exactly how you dominate TikTok, YouTube Shorts, and Instagram Reels in 2026.",
            "segments": [
                {
                    "start": 0.0,
                    "end": 8.5,
                    "speaker": 1,
                    "text": "The absolute craziest thing happened when we started this journey.",
                    "words": [
                        {"word": "The", "start": 0.0, "end": 0.4},
                        {"word": "absolute", "start": 0.4, "end": 1.1},
                        {"word": "craziest", "start": 1.1, "end": 1.8},
                        {"word": "thing", "start": 1.8, "end": 2.2},
                        {"word": "happened", "start": 2.2, "end": 2.9},
                        {"word": "when", "start": 2.9, "end": 3.2},
                        {"word": "we", "start": 3.2, "end": 3.5},
                        {"word": "started", "start": 3.5, "end": 4.1},
                        {"word": "this", "start": 4.1, "end": 4.4},
                        {"word": "journey.", "start": 4.4, "end": 5.2}
                    ]
                },
                {
                    "start": 5.4,
                    "end": 15.2,
                    "speaker": 1,
                    "text": "Nobody believed that AI could literally cut 3-hour podcasts into viral shorts in 10 seconds.",
                    "words": [
                        {"word": "Nobody", "start": 5.4, "end": 6.0},
                        {"word": "believed", "start": 6.0, "end": 6.6},
                        {"word": "that", "start": 6.6, "end": 6.9},
                        {"word": "AI", "start": 6.9, "end": 7.3},
                        {"word": "could", "start": 7.3, "end": 7.6},
                        {"word": "literally", "start": 7.6, "end": 8.2},
                        {"word": "cut", "start": 8.2, "end": 8.6},
                        {"word": "3-hour", "start": 8.6, "end": 9.2},
                        {"word": "podcasts", "start": 9.2, "end": 9.9},
                        {"word": "into", "start": 9.9, "end": 10.3},
                        {"word": "viral", "start": 10.3, "end": 10.8},
                        {"word": "shorts", "start": 10.8, "end": 11.4},
                        {"word": "in", "start": 11.4, "end": 11.7},
                        {"word": "10", "start": 11.7, "end": 12.1},
                        {"word": "seconds.", "start": 12.1, "end": 12.9}
                    ]
                },
                {
                    "start": 15.5,
                    "end": 26.8,
                    "speaker": 2,
                    "text": "Look at MrBeast, Joe Rogan, Lex Fridman. Their short clips get 10 times more views than full episodes!",
                    "words": [
                        {"word": "Look", "start": 15.5, "end": 15.9},
                        {"word": "at", "start": 15.9, "end": 16.2},
                        {"word": "MrBeast,", "start": 16.2, "end": 16.9},
                        {"word": "Joe", "start": 16.9, "end": 17.3},
                        {"word": "Rogan,", "start": 17.3, "end": 17.9},
                        {"word": "Lex", "start": 17.9, "end": 18.3},
                        {"word": "Fridman.", "start": 18.3, "end": 18.9},
                        {"word": "Their", "start": 19.1, "end": 19.5},
                        {"word": "short", "start": 19.5, "end": 19.9},
                        {"word": "clips", "start": 19.9, "end": 20.4},
                        {"word": "get", "start": 20.4, "end": 20.8},
                        {"word": "10", "start": 20.8, "end": 21.2},
                        {"word": "times", "start": 21.2, "end": 21.7},
                        {"word": "more", "start": 21.7, "end": 22.1},
                        {"word": "views", "start": 22.1, "end": 22.6},
                        {"word": "than", "start": 22.6, "end": 22.9},
                        {"word": "full", "start": 22.9, "end": 23.3},
                        {"word": "episodes!", "start": 23.3, "end": 24.1}
                    ]
                },
                {
                    "start": 27.0,
                    "end": 37.8,
                    "speaker": 1,
                    "text": "Wait, do you actually think short-form content is destroying long-form attention spans?",
                    "words": [
                        {"word": "Wait,", "start": 27.0, "end": 27.5},
                        {"word": "do", "start": 27.5, "end": 27.8},
                        {"word": "you", "start": 27.8, "end": 28.1},
                        {"word": "actually", "start": 28.1, "end": 28.7},
                        {"word": "think", "start": 28.7, "end": 29.1},
                        {"word": "short-form", "start": 29.1, "end": 29.9},
                        {"word": "content", "start": 29.9, "end": 30.5},
                        {"word": "is", "start": 30.5, "end": 30.8},
                        {"word": "destroying", "start": 30.8, "end": 31.6},
                        {"word": "long-form", "start": 31.6, "end": 32.3},
                        {"word": "attention", "start": 32.3, "end": 33.0},
                        {"word": "spans?", "start": 33.0, "end": 33.8}
                    ]
                },
                {
                    "start": 38.0,
                    "end": 50.2,
                    "speaker": 2,
                    "text": "That is a complete myth! Short clips actually act as the top of the funnel to bring millions of people back into deep 3-hour conversations.",
                    "words": [
                        {"word": "That", "start": 38.0, "end": 38.3},
                        {"word": "is", "start": 38.3, "end": 38.6},
                        {"word": "a", "start": 38.6, "end": 38.8},
                        {"word": "complete", "start": 38.8, "end": 39.4},
                        {"word": "myth!", "start": 39.4, "end": 40.1},
                        {"word": "Short", "start": 40.3, "end": 40.7},
                        {"word": "clips", "start": 40.7, "end": 41.2},
                        {"word": "actually", "start": 41.2, "end": 41.7},
                        {"word": "act", "start": 41.7, "end": 42.1},
                        {"word": "as", "start": 42.1, "end": 42.4},
                        {"word": "the", "start": 42.4, "end": 42.6},
                        {"word": "top", "start": 42.6, "end": 43.0},
                        {"word": "of", "start": 43.0, "end": 43.3},
                        {"word": "the", "start": 43.3, "end": 43.5},
                        {"word": "funnel", "start": 43.5, "end": 44.1},
                        {"word": "to", "start": 44.1, "end": 44.3},
                        {"word": "bring", "start": 44.3, "end": 44.7},
                        {"word": "millions", "start": 44.7, "end": 45.3},
                        {"word": "of", "start": 45.3, "end": 45.5},
                        {"word": "people", "start": 45.5, "end": 46.0},
                        {"word": "back", "start": 46.0, "end": 46.4},
                        {"word": "into", "start": 46.4, "end": 46.8},
                        {"word": "deep", "start": 46.8, "end": 47.3},
                        {"word": "3-hour", "start": 47.3, "end": 48.0},
                        {"word": "conversations.", "start": 48.0, "end": 49.0}
                    ]
                },
                {
                    "start": 50.5,
                    "end": 64.0,
                    "speaker": 1,
                    "text": "The secret is the hook. In the first 3 seconds, if you don't shock them or make them curious, they swipe away.",
                    "words": [
                        {"word": "The", "start": 50.5, "end": 50.8},
                        {"word": "secret", "start": 50.8, "end": 51.4},
                        {"word": "is", "start": 51.4, "end": 51.7},
                        {"word": "the", "start": 51.7, "end": 52.0},
                        {"word": "hook.", "start": 52.0, "end": 52.7},
                        {"word": "In", "start": 52.9, "end": 53.2},
                        {"word": "the", "start": 53.2, "end": 53.4},
                        {"word": "first", "start": 53.4, "end": 53.8},
                        {"word": "3", "start": 53.8, "end": 54.2},
                        {"word": "seconds,", "start": 54.2, "end": 54.9},
                        {"word": "if", "start": 55.0, "end": 55.3},
                        {"word": "you", "start": 55.3, "end": 55.5},
                        {"word": "don't", "start": 55.5, "end": 56.0},
                        {"word": "shock", "start": 56.0, "end": 56.6},
                        {"word": "them", "start": 56.6, "end": 57.0},
                        {"word": "or", "start": 57.0, "end": 57.3},
                        {"word": "make", "start": 57.3, "end": 57.7},
                        {"word": "them", "start": 57.7, "end": 58.1},
                        {"word": "curious,", "start": 58.1, "end": 58.8},
                        {"word": "they", "start": 58.9, "end": 59.2},
                        {"word": "swipe", "start": 59.2, "end": 59.8},
                        {"word": "away.", "start": 59.8, "end": 60.5}
                    ]
                }
            ]
        }
    },
    {
        "id": "demo_podcast_hindi_02",
        "title": "Success Mindset & Discipline Secrets (Hindi / Hinglish Special)",
        "source_type": "upload",
        "duration": 150.0,
        "language": "hi",
        "speaker_count": 2,
        "speakers": ["Ranveer", "Dr. Vikas"],
        "thumbnail": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=800&auto=format&fit=crop&q=80",
        "transcript": {
            "language": "hi",
            "duration": 150.0,
            "text": "अगर आप जीवन में सफल होना चाहते हैं तो सबसे बड़ा सीक्रेट है कंसिस्टेंसी। लोग सोचते हैं कि मोटिवेशन से काम होगा, लेकिन असली ताकत अनुशासन में है। जब आपका मूड ना हो तब भी काम करना ही असली विनर की पहचान है।",
            "segments": [
                {
                    "start": 0.0,
                    "end": 8.0,
                    "speaker": 1,
                    "text": "अगर आप जीवन में सफल होना चाहते हैं तो सबसे बड़ा सीक्रेट है कंसिस्टेंसी।",
                    "words": [
                        {"word": "अगर", "start": 0.0, "end": 0.5},
                        {"word": "आप", "start": 0.5, "end": 0.8},
                        {"word": "जीवन", "start": 0.8, "end": 1.4},
                        {"word": "में", "start": 1.4, "end": 1.7},
                        {"word": "सफल", "start": 1.7, "end": 2.3},
                        {"word": "होना", "start": 2.3, "end": 2.8},
                        {"word": "चाहते", "start": 2.8, "end": 3.4},
                        {"word": "हैं", "start": 3.4, "end": 3.7},
                        {"word": "तो", "start": 3.7, "end": 4.0},
                        {"word": "सबसे", "start": 4.0, "end": 4.6},
                        {"word": "बड़ा", "start": 4.6, "end": 5.1},
                        {"word": "सीक्रेट", "start": 5.1, "end": 5.8},
                        {"word": "है", "start": 5.8, "end": 6.1},
                        {"word": "कंसिस्टेंसी।", "start": 6.1, "end": 7.2}
                    ]
                },
                {
                    "start": 8.5,
                    "end": 18.0,
                    "speaker": 2,
                    "text": "लोग सोचते हैं कि मोटिवेशन से काम होगा, लेकिन असली ताकत अनुशासन में है।",
                    "words": [
                        {"word": "लोग", "start": 8.5, "end": 9.0},
                        {"word": "सोचते", "start": 9.0, "end": 9.7},
                        {"word": "हैं", "start": 9.7, "end": 10.0},
                        {"word": "कि", "start": 10.0, "end": 10.3},
                        {"word": "मोटिवेशन", "start": 10.3, "end": 11.2},
                        {"word": "से", "start": 11.2, "end": 11.5},
                        {"word": "काम", "start": 11.5, "end": 12.0},
                        {"word": "होगा,", "start": 12.0, "end": 12.6},
                        {"word": "लेकिन", "start": 12.8, "end": 13.4},
                        {"word": "असली", "start": 13.4, "end": 14.0},
                        {"word": "ताकत", "start": 14.0, "end": 14.6},
                        {"word": "अनुशासन", "start": 14.6, "end": 15.6},
                        {"word": "में", "start": 15.6, "end": 15.9},
                        {"word": "है।", "start": 15.9, "end": 16.5}
                    ]
                }
            ]
        }
    }
]

def generate_sample_mp4(output_path: str, duration: int = 65):
    """
    Creates a studio podcast test MP4 with synthetic dual audio tone
    and animated visualizer frame using FFmpeg testsrc.
    """
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        return output_path

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={duration}:size=1920x1080:rate=30",
        "-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf", "drawbox=x=0:y=0:w=1920:h=1080:color=black@0.6:t=fill",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        pass
    return output_path
