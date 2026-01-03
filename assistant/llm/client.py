from __future__ import annotations

from typing import Dict, List, Optional

from assistant.config import ASSISTANT_NAME, ASSISTANT_MISSION


class LLMClient:
    """
    LLMClient v1 (stable scaffold)
    - Builds a mission-aligned prompt using: screen context, memory, and optional web sources.
    - Returns a structured response: {answer, confidence, sources_used, uncertainties}.

    NOTE:
    `generate()` is currently a friendly stub so your system remains stable while you iterate.
    When you're ready, swap `generate()` with a real model call (API or local).
    """

    def __init__(self, debug_prompts: bool = False):
        self.debug_prompts = debug_prompts

    # -----------------------
    # Public API
    # -----------------------
    def respond(
        self,
        user_input: str,
        screen_context: Dict,
        memory_text: str = "",
        web_sources: Optional[List[Dict[str, str]]] = None,
        web_prompt_block: str = "",
    ) -> Dict:
        web_sources = web_sources or []

        prompt = self._build_prompt(
            user_input=user_input,
            screen_context=screen_context,
            memory_text=memory_text,
            web_prompt_block=web_prompt_block,
        )

        if self.debug_prompts:
            print("\n--- PROMPT SENT TO LLM ---")
            print(prompt)
            print("--- END PROMPT ---\n")

        answer_text = self.generate(prompt, user_input=user_input, screen_context=screen_context, web_sources=web_sources)
        answer_text = (answer_text or "").strip()

        confidence, uncertainties = self._estimate_confidence(
            user_input=user_input,
            screen_context=screen_context,
            web_sources=web_sources,
            answer_text=answer_text,
        )

        sources_used = [{"title": s.get("title", ""), "url": s.get("url", "")} for s in web_sources]

        return {
            "answer": answer_text,
            "confidence": confidence,
            "sources_used": sources_used,
            "uncertainties": uncertainties,
        }

    # -----------------------
    # Model call (stub for now)
    # -----------------------
    def generate(
        self,
        prompt: str,
        user_input: str,
        screen_context: Dict,
        web_sources: List[Dict[str, str]],
    ) -> str:
        """
        Friendly placeholder response generator.

        This keeps VERA feeling natural even before you plug in a real model.
        It uses the user's request + whatever context is available to respond in a grounded way.
        """
        text = (user_input or "").strip().lower()

        detected = (screen_context.get("detected_text") or "").strip()
        has_screen = bool(detected)
        has_web = any((s.get("text") or "").strip() for s in web_sources)

        # If the user is asking about purpose/identity, keep it warm and direct
        if any(p in text for p in ["your purpose", "your mission", "what are you", "who are you"]):
            return f"{ASSISTANT_MISSION}"

        # If they ask "what's on my screen" but OCR isn't available, be transparent
        if "on my screen" in text or "on the screen" in text or "what's happening" in text:
            if has_screen:
                return f"Alright — here’s what I’m seeing on your screen:\n\n{detected}"
            return (
                "I’m not getting readable text from the screen yet (OCR isn’t available), "
                "but if you tell me which app/window you’re focused on, I can still help. "
                "Also, once OCR is set up, I’ll be able to describe what I’m seeing more precisely."
            )

        # If they asked for web info and we have sources, acknowledge it
        if has_web:
            top = web_sources[0]
            title = top.get("title", "a source").strip()
            return (
                f"Got it. I pulled a few sources to help.\n\n"
                f"Here’s the gist based on what I found: {self._friendly_summary_from_sources(web_sources)}\n\n"
                f"If you want, I can zoom in on details from “{title}”."
            )

        # Default: friendly, helpful, non-robotic
        return (
            "Okay, Tell me what you want to do next, and I’ll help you get there. "
            "If you want me to base it on your screen, tell me which window you’re looking at."
        )

    # -----------------------
    # Prompt building
    # -----------------------
    def _build_prompt(
        self,
        user_input: str,
        screen_context: Dict,
        memory_text: str,
        web_prompt_block: str,
    ) -> str:
        # Keep it mission-aligned, calm, and honest.
        # This prompt is designed so when you swap in a real LLM, behavior remains consistent.
        return (
            f"SYSTEM:\n"
            f"You are {ASSISTANT_NAME}.\n\n"
            f"MISSION:\n"
            f"{ASSISTANT_MISSION}\n\n"
            f"STYLE:\n"
            f"- Friendly, calm, and human.\n"
            f"- Clear and practical.\n"
            f"- If unsure, say so.\n"
            f"- Do not invent facts.\n\n"
            f"SCREEN CONTEXT (summary):\n"
            f"{screen_context}\n\n"
            f"RECENT MEMORY:\n"
            f"{memory_text}\n\n"
            f"USER SAID:\n"
            f"{user_input}\n\n"
            f"WEB SOURCES (optional):\n"
            f"{web_prompt_block}\n\n"
            f"TASK:\n"
            f"Respond helpfully and accurately. If web sources are present, use them.\n"
        )

    # -----------------------
    # Confidence + uncertainty
    # -----------------------
    def _estimate_confidence(
        self,
        user_input: str,
        screen_context: Dict,
        web_sources: List[Dict[str, str]],
        answer_text: str,
    ) -> (float, List[str]):
        """
        Simple, transparent heuristic confidence.
        You can replace this later with model self-rating if you want.
        """
        uncertainties: List[str] = []

        detected = (screen_context.get("detected_text") or "").strip()
        has_screen = bool(detected)
        has_web = any((s.get("text") or "").strip() for s in web_sources)

        confidence = 0.55

        if has_screen:
            confidence += 0.15
        else:
            # If user asked about screen and we have no screen text, reduce
            low = (user_input or "").lower()
            if "screen" in low or "on my screen" in low or "what's happening" in low:
                confidence -= 0.20
                uncertainties.append("I don’t have readable screen text right now (OCR may be missing).")

        if has_web:
            confidence += 0.25

        # If answer is super generic, slightly lower confidence
        if len(answer_text.split()) < 12:
            confidence -= 0.05

        confidence = max(0.0, min(1.0, confidence))
        return confidence, uncertainties

    # -----------------------
    # Tiny helper for friendly web summary (stub)
    # -----------------------
    def _friendly_summary_from_sources(self, web_sources: List[Dict[str, str]]) -> str:
        """
        A lightweight fallback summarizer so VERA doesn't sound robotic.
        This is NOT a real summarizer; it just extracts a bit of text to show progress.
        Replace with an LLM summarization step later.
        """
        for s in web_sources:
            txt = (s.get("text") or "").strip()
            if txt:
                # Return a short slice that feels like a "gist"
                return txt[:220].rstrip() + "..."
        return "I couldn’t extract clean text from the sources, but I can still open them and work from titles/URLs."

