# assistant/config.py

ASSISTANT_NAME = "VERA"

ASSISTANT_MISSION = (
    "I'm VERA, a Voice-Enabled Reasoning Assistant designed to keep you moving. "
    "I understand what you say, what you're looking at, and what's coming next. "
    "I organize your day, anticipate priorities, and offer real-time guidance "
    "without distraction so you can stay focused and in execution mode."
)

# Wake words / aliases (lowercase)
WAKE_WORDS = [
    "hey vera",
    "vera",
]

# Sleep phrases (lowercase)
SLEEP_PHRASES = [
    "go to sleep",
    "sleep",
    "stand by",
    "pause listening",
]


# ---------------------------
# Voice configuration
# ---------------------------

ASSISTANT_VOICE_NAME = "Ava"  # macOS voice name
ASSISTANT_VOICE_RATE = 136         # words per minute (lower = calmer)
ASSISTANT_VOICE_VOLUME = 1.0       # 0.0 – 1.0

DEMO_MODE = True
