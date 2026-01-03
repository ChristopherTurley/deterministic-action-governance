# context.py
import pytesseract
import cv2

class ContextBuilder:
    def extract_text(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)

    def build(self, text):
        context = {
            "tickers": [],
            "numbers": [],
            "raw": text
        }

        for line in text.split("\n"):
            if "PLTR" in line:
                context["tickers"].append("PLTR")
            if any(c.isdigit() for c in line):
                context["numbers"].append(line.strip())

        return context
