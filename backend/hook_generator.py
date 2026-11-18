import re
from typing import Dict, Any, List

class ViralHookGenerator:
    """
    Generates high-CTR viral hooks, titles, captions, hashtags,
    and platform-specific variations for YouTube Shorts, TikTok,
    Instagram Reels, LinkedIn, and X/Twitter.
    """

    HOOK_TEMPLATES = {
        "shocking": [
            "Watch what happens when nobody is watching...",
            "They didn't want this footage to leak...",
            "The 1 thing they never told you about this 😱",
            "I couldn't believe what he said next...",
            "Wait for the reaction at the end 💀"
        ],
        "controversial": [
            "Unpopular opinion, but someone had to say it 🤫",
            "99% of people are completely wrong about this.",
            "Stop doing this immediately if you want to grow.",
            "Why the entire industry is lying to you 🚨",
            "This will probably get me canceled, but..."
        ],
        "funny": [
            "Bro thought he could get away with this 😂💀",
            "I literally choked on my water when he said this 🤣",
            "Tell me you didn't just hear that?! 😭",
            "Most unhinged podcast moment of the year 💀",
            "He had ZERO hesitation saying that 😂"
        ],
        "powerful_speech": [
            "Save this video for the days you want to quit 💪",
            "The 1 rule that separates the top 1% from everyone else.",
            "If you only watch one video today, make it this one 🔥",
            "Listen to this until it clicks in your mind 🧠",
            "This 30-second speech will shift your entire mindset."
        ],
        "interesting_fact": [
            "You won't believe how your brain actually works 🤯",
            "This 1 statistical anomaly will blow your mind 💡",
            "Science just proved what everyone thought was impossible.",
            "Did you know 85% of people do this without realizing?",
            "The hidden psychology behind why we do this."
        ],
        "argument": [
            "The moment things got REALLY personal... 🥊",
            "You can literally feel the tension through the screen.",
            "He tried to defend himself and completely failed 😬",
            "Watch his facial expression when he gets called out 😳",
            "When two experts completely clash on live air."
        ],
        "emotional": [
            "This will hit you right in the heart ❤️🥺",
            "The hardest lesson anyone ever has to learn...",
            "I was not prepared for this level of honesty 💔",
            "You never know what someone is going through inside.",
            "The most vulnerable conversation on this podcast."
        ]
    }

    HASHTAG_PACKS = {
        "shocking": ["#viral", "#shorts", "#reels", "#fyp", "#podcastclips", "#mindblown", "#shocking", "#trending"],
        "controversial": ["#debate", "#truth", "#unpopularopinion", "#hotfood", "#podcast", "#shorts", "#mindset"],
        "funny": ["#funny", "#lol", "#meme", "#streamer", "#podcastmoment", "#hilarious", "#gaming", "#reaction"],
        "powerful_speech": ["#motivation", "#mindset", "#discipline", "#success", "#inspiration", "#entrepreneur", "#grind"],
        "interesting_fact": ["#didyouknow", "#facts", "#science", "#psychology", "#learnontiktok", "#education", "#deepdive"],
        "argument": ["#drama", "#clash", "#podcastdebate", "#interview", "#viralmoment", "#exposed", "#talkshow"],
        "emotional": ["#heartwarming", "#deepconversations", "#lifelessons", "#empathy", "#vulnerability", "#podcastvibes"]
    }

    @classmethod
    def generate_all(cls, clip_text: str, category: str = "shocking", viral_score: int = 85) -> Dict[str, Any]:
        """
        Generates full viral packaging for a clip.
        """
        cat_key = category if category in cls.HOOK_TEMPLATES else "shocking"
        hooks = cls.HOOK_TEMPLATES[cat_key]
        hashtags = cls.HASHTAG_PACKS[cat_key]

        words = clip_text.split()
        summary_snippet = " ".join(words[:12]) + "..." if len(words) > 12 else clip_text

        primary_hook = hooks[0]
        opening_overlay = hooks[1] if len(hooks) > 1 else primary_hook

        # Clean title
        clean_first_phrase = " ".join(words[:6]).replace('"', '').replace("'", "")
        title = f"{primary_hook.replace('...', '')} | {clean_first_phrase}"

        # Short social caption
        caption = f"{primary_hook}\n\n\"{summary_snippet}\"\n\nDrop your thoughts in the comments! 👇 {' '.join(hashtags[:5])}"

        # Platform specific variations
        platform_variations = {
            "tiktok": {
                "platform": "TikTok",
                "char_limit": "2,200",
                "recommended_ratio": "9:16",
                "text": f"{hooks[0]}\n\nWatch till the end! 😱\n\n{' '.join(hashtags[:6])} #fypシ #viralvideo"
            },
            "instagram_reels": {
                "platform": "Instagram Reels",
                "char_limit": "2,200",
                "recommended_ratio": "9:16",
                "text": f"Wait until the end... 🤯\n\nFollow @streamclip.ai for daily high-impact podcast gems! ✨\n\nShare this with someone who needs to hear it. 📲\n\n{' '.join(hashtags)}"
            },
            "youtube_shorts": {
                "platform": "YouTube Shorts",
                "char_limit": "100",
                "recommended_ratio": "9:16",
                "text": f"{primary_hook} 😱 #Shorts #Podcast #Viral"
            },
            "x_twitter": {
                "platform": "X (Twitter)",
                "char_limit": "280",
                "recommended_ratio": "16:9 / 1:1",
                "text": f"This 30-second moment from the latest podcast episode says it all:\n\n\"{summary_snippet}\"\n\nDo you agree or disagree? 🧵👇"
            },
            "linkedin": {
                "platform": "LinkedIn",
                "char_limit": "3,000",
                "recommended_ratio": "1:1 / 4:5",
                "text": f"Key takeaway from an incredible discussion:\n\n\"{clip_text}\"\n\nIn business and life, perspective shifts happen when you question default assumptions.\n\nWhat is your perspective on this? Let's discuss in the comments.\n\n#Leadership #PersonalDevelopment #PodcastTakeaways"
            }
        }

        return {
            "hook": primary_hook,
            "opening_overlay_text": opening_overlay,
            "title": title,
            "social_caption": caption,
            "hashtags": hashtags,
            "hooks_alternatives": hooks,
            "platform_variations": platform_variations
        }
