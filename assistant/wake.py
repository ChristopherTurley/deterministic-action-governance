from assistant.config import WAKE_WORDS, SLEEP_PHRASES

class WakeDetector:
    def __init__(self):
        self.wake_words = [w.lower() for w in WAKE_WORDS]
        self.sleep_phrases = [s.lower() for s in SLEEP_PHRASES]

    def is_wake(self, transcript: str) -> bool:
        t = (transcript or "").lower()
        return any(w in t for w in self.wake_words)

    def is_sleep(self, transcript: str) -> bool:
        t = (transcript or "").lower()
        return any(s in t for s in self.sleep_phrases)

