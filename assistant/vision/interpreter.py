import pytesseract
import cv2

class ScreenInterpreter:
    def summarize(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

        summary = {
            "detected_text": text[:500],
            "visual_guess": self._guess_activity(text)
        }
        return summary

    def _guess_activity(self, text):
        t = text.lower()
        if "chart" in t or "price" in t:
            return "monitoring a chart"
        if "code" in t or "import" in t:
            return "working with code"
        if "mail" in t or "inbox" in t:
            return "reading email"
        return "general screen activity"
